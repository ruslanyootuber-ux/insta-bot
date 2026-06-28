# handlers/hadis_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
import random
from data.hadis_data import HADISLAR
from keyboards.hadis_kb import get_hadis_keyboard

router = Router()

@router.callback_query(F.data == "menu_hadis")
async def show_random_hadis(callback: CallbackQuery):
    await callback.answer() 

    index = random.randint(0, len(HADISLAR) - 1)
    hadis = HADISLAR[index]

    text = f"📖 <b>Kun hadisi:</b>\n\n<i>{hadis['uzbek']}</i>\n\nQuyidagi tugmalardan birini tanlab matnni o'qing:"

    await callback.message.edit_text(text, reply_markup=get_hadis_keyboard(index), parse_mode="HTML")

@router.callback_query(F.data.startswith("h_"))
async def show_hadis_text(callback: CallbackQuery):
    await callback.answer() 

    parts = callback.data.split("_")
    mode = parts[1] # ar, lat, kir
    index = int(parts[2])
    hadis = HADISLAR[index]

    mapping = {
        "ar": ("🇸🇦 Arabcha", hadis['arabic']), 
        "lat": ("🇺🇿 Lotin", hadis['latin']), 
        "kir": ("🇷🇺 Kirill", hadis['cyrillic'])
    }

    title, content = mapping[mode]
    text = f"📖 <b>{title}:</b>\n\n{content}\n\n<i>{hadis['uzbek']}</i>"

    await callback.message.edit_text(text, reply_markup=get_hadis_keyboard(index), parse_mode="HTML")
