from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from loader import db 
from keyboards.callbacks import RegionCallback, DistrictCallback
from keyboards.inline_kb import get_regions_keyboard, get_districts_keyboard
from utils.aladhan_api import get_prayer_times

router = Router()

@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    # Callbackni yopish (qotib qolmasligi uchun)
    await callback.answer()
    
    region_name = callback_data.region_name
    text = f"📍 <b>{region_name}</b>ni tanladingiz.\n\n🏙 Endi tumanni tanlang:"
    await callback.message.edit_text(text=text, reply_markup=get_districts_keyboard(region_name))

@router.callback_query(F.data == "back_to_regions")
async def process_back_to_regions(callback: CallbackQuery):
    # Callbackni yopish
    await callback.answer()
    
    text = "👇 <i>Iltimos, o'zingizga kerakli viloyatni tanlang:</i>"
    await callback.message.edit_text(text=text, reply_markup=get_regions_keyboard())

@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    # Callbackni yopish
    await callback.answer()
    
    district_name = callback_data.district_name
    db.update_district(callback.from_user.id, district_name)
    
    # Bazadan mazhabni olamiz
    user_data = db.get_user_data(callback.from_user.id)
    school = user_data[4] if user_data else 0
    
    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yuklanmoqda...</i>")

    # API ga mazhabni yuboramiz
    times = await get_prayer_times(district_name, school=school)

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")

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