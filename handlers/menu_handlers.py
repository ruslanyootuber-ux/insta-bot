from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from loader import db 
from keyboards.callbacks import RegionCallback, DistrictCallback
from keyboards.inline_kb import get_regions_keyboard, get_districts_keyboard
from utils.aladhan_api import get_prayer_times

router = Router()

# 1. Asosiy menyuga qaytish (Viloyatlar ro'yxati)
@router.callback_query(F.data.in_(["back_to_regions", "back_to_menu"]))
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    text = "👇 <i>Iltimos, o'zingizga kerakli viloyatni tanlang:</i>"
    await callback.message.edit_text(text=text, reply_markup=get_regions_keyboard())

# 2. Viloyat tanlanganda
@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    await callback.answer()
    region_name = callback_data.region_name
    text = f"📍 <b>{region_name}</b>ni tanladingiz.\n\n🏙 Endi tumanni tanlang:"
    await callback.message.edit_text(text=text, reply_markup=get_districts_keyboard(region_name))

# 3. Tuman tanlanganda
@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    await callback.answer()
    
    district_name = callback_data.district_name
    db.update_district(callback.from_user.id, district_name)
    
    user_data = db.get_user_data(callback.from_user.id)
    school = user_data[4] if user_data else 0
    
    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yuklanmoqda...</i>")

    times = await get_prayer_times(district_name, school=school)

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_menu")

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
        text = "❌ Xatolik yuz berdi."

    await callback.message.edit_text(text, reply_markup=builder.as_markup())