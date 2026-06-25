from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from keyboards.callbacks import RegionCallback, DistrictCallback
from keyboards.inline_kb import get_regions_keyboard, get_districts_keyboard
from utils.aladhan_api import get_prayer_times

router = Router()

# Viloyat tanlanganda tumanlarni chiqarish
@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    region_name = callback_data.region_name
    text = f"📍 <b>{region_name}</b>ni tanladingiz.\n\n🏙 Endi tumanni tanlang:"
    
    await callback.message.edit_text(
        text=text,
        reply_markup=get_districts_keyboard(region_name)
    )

# "Orqaga" tugmasi bosilganda viloyatlarga qaytish
@router.callback_query(F.data == "back_to_regions")
async def process_back_to_regions(callback: CallbackQuery):
    text = "👇 <i>Iltimos, o'zingizga kerakli viloyatni tanlang:</i>"
    await callback.message.edit_text(
        text=text,
        reply_markup=get_regions_keyboard()
    )

# Tuman tanlanganda API dan vaqtni olib kelish
@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    district_name = callback_data.district_name
  # BAZAGA YOZISH:
db.update_district(callback.from_user.id, district_name)
    
    # Foydalanuvchiga kutib turishni aytamiz (chunki API so'rov 1-2 soniya oladi)
    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yuklanmoqda...</i>")
    
    # API ga so'rov yuboramiz
    times = await get_prayer_times(district_name)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    
    if times:
        today = datetime.now().strftime("%d.%m.%Y")
        text = (
            f"🕌 <b>{district_name}</b> uchun namoz vaqtlari:\n"
            f"📅 Sana: {today}\n\n"
            f"🌅 <b>Bomdod:</b> {times['Bomdod']}\n"
            f"🌄 <b>Quyosh:</b> {times['Quyosh']}\n"
            f"☀️ <b>Peshin:</b> {times['Peshin']}\n"
            f"🌤 <b>Asr:</b> {times['Asr']}\n"
            f"🌇 <b>Shom:</b> {times['Shom']}\n"
            f"🌌 <b>Xufton:</b> {times['Xufton']}\n\n"
            f"<i>Manba: Aladhan API</i>"
        )
    else:
        text = "❌ Kechirasiz, API serveri bilan bog'lanishda xatolik yuz berdi. Iltimos keyinroq urinib ko'ring."
        
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
