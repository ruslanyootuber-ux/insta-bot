from aiogram import Router, F
from aiogram.types import CallbackQuery
from loader import db, bot
from utils.aladhan_api import get_prayer_times
from data.ramadan_data import SAHARLIK_DUO, IFTORLIK_DUO
from keyboards.ramadan_kb import get_ramadan_keyboard

router = Router()

@router.callback_query(F.data == "menu_ramadan")
async def process_ramadan_menu(callback: CallbackQuery):
    await callback.message.edit_text("🌙 <b>Ramazon bo'limi</b>\n\nKerakli bo'limni tanlang:", reply_markup=get_ramadan_keyboard())

@router.callback_query(F.data == "ramadan_today")
async def process_ramadan_today(callback: CallbackQuery):
    user_data = db.get_user_data(callback.from_user.id)
    district = user_data[2] # Bazadan viloyat/tuman
    
    if not district:
        await callback.answer("❌ Avval viloyatni tanlang!", show_alert=True)
        return

    times = await get_prayer_times(district)
    # Ramazonda: Saharlik = Bomdod vaqti, Iftorlik = Shom vaqti
    text = f"📅 <b>Bugungi Ramazon vaqtlari ({district})</b>\n\n🌅 Saharlik (og'iz yopish): {times.get('Bomdod')}\n🌇 Iftorlik (og'iz ochish): {times.get('Shom')}"
    await callback.message.edit_text(text, reply_markup=get_ramadan_keyboard())

@router.callback_query(F.data == "ramadan_duas")
async def process_ramadan_duas(callback: CallbackQuery):
    await callback.message.edit_text(f"{SAHARLIK_DUO}\n\n{IFTORLIK_DUO}", reply_markup=get_ramadan_keyboard())