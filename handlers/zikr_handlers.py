# handlers/zikr_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.zikr_kb import get_zikr_main_keyboard, get_zikr_pagination_keyboard
from data.zikr_data import MORNING_ZIKRS, EVENING_ZIKRS

router = Router()

# Asosiy menyudan Zikrlar bo'limiga kirish
@router.callback_query(F.data == "menu_zikr_main")
async def process_zikr_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🤲 <b>Tonggi va Kechki zikrlar</b>\n\nQaysi vaqt zikrlarini o'qishni xohlaysiz?",
        reply_markup=get_zikr_main_keyboard(),
        parse_mode="HTML"
    )

# Tonggi yoki Kechki zikrlarni boshlash (har doim 0-indeksdan boshlanadi)
@router.callback_query(F.data.startswith("zikr_start_"))
async def start_zikr_reading(callback: CallbackQuery):
    await callback.answer()
    z_type = callback.data.split("_")[2] # "morning" yoki "evening"
    await show_zikr_page(callback, z_type, 0)

# Varaqlash tugmalari bosilganda
@router.callback_query(F.data.startswith("zikr_morning_") | F.data.startswith("zikr_evening_"))
async def paginate_zikrs(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split("_")
    z_type = parts[1] # "morning" yoki "evening"
    index = int(parts[2]) # Sahifa raqami
    await show_zikr_page(callback, z_type, index)

# O'lik tugmalar bosilganda (masalan 1/10 degan yozuvli tugma) qotib qolmasligi uchun
@router.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()

# Asosiy xabarni yangilovchi yordamchi funksiya
async def show_zikr_page(callback: CallbackQuery, z_type: str, index: int):
    zikrs = MORNING_ZIKRS if z_type == "morning" else EVENING_ZIKRS
    total = len(zikrs)

    current_zikr = zikrs[index]
    title = "🌅 Tonggi zikrlar" if z_type == "morning" else "🌇 Kechki zikrlar"

    text = (
        f"<b>{title}</b>\n\n"
        f"🔤 <b>Arabcha:</b>\n{current_zikr['arabic']}\n\n"
        f"🗣 <b>O'qilishi:</b>\n<i>{current_zikr['translit']}</i>\n\n"
        f"🇺🇿 <b>Ma'nosi:</b>\n{current_zikr['uzbek']}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=get_zikr_pagination_keyboard(z_type, index, total),
        parse_mode="HTML"
    )
