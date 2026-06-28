from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from loader import db 
from keyboards.callbacks import RegionCallback, DistrictCallback
from keyboards.inline_kb import get_regions_keyboard, get_districts_keyboard, get_main_menu_kb # <-- get_main_menu_kb қўшилди
from utils.aladhan_api import get_prayer_times

router = Router()

# 1. Асосий менюга батамом қайтиш (Ботнинг бош менюсига)
@router.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: CallbackQuery):
    await callback.answer()
    text = "🕌 <b>Асосий меню</b>\n\nКеракли бўлимни танланг:"
    try:
        # Агар хабар матнли бўлса, шунчаки ўзгартирамиз
        await callback.message.edit_text(text=text, reply_markup=get_main_menu_kb(), parse_mode="HTML")
    except Exception:
        # Агар аудио ёки бошқа форматдан қайтилаётган бўлса, эскисини ўчириб янгисини юборамиз
        await callback.message.delete()
        await callback.message.answer(text=text, reply_markup=get_main_menu_kb(), parse_mode="HTML")

# 2. Намоз вақтлари ичидан Вилоятлар рўйхатига қайтиш
@router.callback_query(F.data.in_(["back_to_regions", "back_to_menu", "menu_regions"]))
async def back_to_menu_regions(callback: CallbackQuery):
    await callback.answer()
    text = "👇 <i>Iltimos, o'zingizga kerakli viloyatni tanlang:</i>"
    try:
        await callback.message.edit_text(text=text, reply_markup=get_regions_keyboard(), parse_mode="HTML")
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=text, reply_markup=get_regions_keyboard(), parse_mode="HTML")

# 3. Вилоят танланганда (Туманлар рўйхати чиқади)
@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    await callback.answer()
    region_name = callback_data.region_name
    text = f"📍 <b>{region_name}</b>ni tanladingiz.\n\n🏙 Endi tumanni tanlang:"
    await callback.message.edit_text(text=text, reply_markup=get_districts_keyboard(region_name), parse_mode="HTML")

# 4. Туман танланганда (Намоз вақтлари чиқади)
@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    await callback.answer()

    district_name = callback_data.district_name
    db.update_district(callback.from_user.id, district_name)

    user_data = db.get_user_data(callback.from_user.id)
    school = user_data[4] if user_data else 0

    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yuklanmoqda...</i>", parse_mode="HTML")

    times = await get_prayer_times(district_name, school=school)

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_menu")
    builder.button(text="🏠 Asosiy menu", callback_data="back_to_main") # <-- Асосий меню тугмаси қўшилди
    builder.adjust(1)

    if times:
        today = datetime.now().strftime("%d.%m.%Y")
        text = (
            f"🕌 <b>{district_name}</b> uchun namoz vaqtlari:\n"
            f"Mazhab: {'Shafi\'i' if school == 1 else 'Hanafi'}\n"
            f"📅 Sana: {today}\n\n"
            f"🌅 <b>Bomdod:</b> {times['Bomdod']}\n"
            f"🌄 <b>Quyosh:</b> {times['Quyosh']}\n"
            f"☀️ <b>Peshin:</b> {times['Peshin']}\n"
            f"🌤 <b>Asr:</b> {times['Asr']}\n"
            f"🌇 <b>Shom:</b> {times['Shom']}\n"
            f"🌌 <b>Xufton:</b> {times['Xufton']}\n\n"
        )
    else:
        text = "❌ Xatolik yuz berdi. Маълумот олишда муаммо юзага келди."

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
