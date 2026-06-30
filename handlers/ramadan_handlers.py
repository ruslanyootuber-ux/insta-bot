# handlers/ramadan_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from loader import bot  # Botni loader'dan olamiz
from database.db import db  # Bazani o'zining faylidan olamiz
from utils.aladhan_api import get_prayer_times
from data.ramadan_data import SAHARLIK_DUO, IFTORLIK_DUO
from keyboards.ramadan_kb import get_ramadan_keyboard

router = Router()

@router.callback_query(F.data == "menu_ramadan")
async def process_ramadan_menu(callback: CallbackQuery):
    await callback.answer() # Соат айланиб қотишини тўхтатади
    await callback.message.edit_text(
        "🌙 <b>Ramazon bo'limi</b>\n\nKerakli bo'limni tanlang:", 
        reply_markup=get_ramadan_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "ramadan_today")
async def process_ramadan_today(callback: CallbackQuery):
    user_data = db.get_user_data(callback.from_user.id)
    
    if not user_data or not user_data[2]:
        await callback.answer("❌ Avval viloyat va tumanni tanlang!", show_alert=True)
        return

    await callback.answer()
    district = user_data[2] # Bazadan viloyat/tuman

    times = await get_prayer_times(district)
    
    if times:
        # Ramazonda: Saharlik = Bomdod vaqti, Iftorlik = Shom vaqti
        text = (
            f"📅 <b>Bugungi Ramazon vaqtlari ({district})</b>\n\n"
            f"🌅 <b>Saharlik (og'iz yopish):</b> {times.get('Bomdod')}\n"
            f"🌇 <b>Iftorlik (og'iz ochish):</b> {times.get('Shom')}"
        )
    else:
        text = "❌ Намоз вақтларини юклашда хатолик юз берди."
        
    await callback.message.edit_text(text, reply_markup=get_ramadan_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "ramadan_duas")
async def process_ramadan_duas(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        f"{SAHARLIK_DUO}\n\n{IFTORLIK_DUO}", 
        reply_markup=get_ramadan_keyboard(),
        parse_mode="HTML"
    )
