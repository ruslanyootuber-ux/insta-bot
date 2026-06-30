# handlers/extra_handlers.py

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import bot
from utils.aladhan_api import get_prayer_times

router = Router()

# --- 1. Avtomatik eslatma tekshiruvi (Scheduler xatolik bermasligi uchun himoyalandi) ---
async def check_and_send_reminders():
    try:
        # Baza o'chirilgani sababli hozircha vaqtincha pass holatida turadi, 
        # lekin har minutda ishlaganda xatolik (Crash) bermaydi.
        pass 
    except Exception as e:
        logging.error(f"Eslatma tekshirishda xatolik yuz berdi: {e}")

# --- 2. Eslatma sozlamalari ---
def get_reminder_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Eslatma funksiyasi vaqtincha ishlamaydi", callback_data="none")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(
            text="🔔 <b>Eslatma sozlamalari</b>\n\n(Baza o'chirilgani uchun bu funksiya hozircha ishlamaydi)", 
            reply_markup=get_reminder_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Eslatma menyusini ochishda xatolik: {e}")

# --- 3. Mazhab sozlamalari ---
@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="🕌 Mazhab: Hanafi", callback_data="no_action")
    builder.button(text="🕋 Mazhab: Shafi'i", callback_data="no_action")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    builder.adjust(1)
    
    try:
        await callback.message.edit_text(
            text="⚙️ <b>Sozlamalar</b>\n\nMazhab tanlash uchun baza talab qilinadi.", 
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Sozlamalar menyusini ochishda xatolik: {e}")

# --- 4. Yaratuvchi bo'limi ---
@router.callback_query(F.data == "menu_creator")
async def process_creator(callback: CallbackQuery):
    await callback.answer()
    text = (
        "👨‍💻 <b>Bot Yaratuvchisi</b>\n\n"
        "Barcha viloyat va tumanlar uchun eng aniq namoz vaqtlari yetkazib berish maqsad qilingan.\n\n"
        "📩 <i>Taklif va murojaatlar uchun pastdagi tugmani bosing:</i>"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Admin bilan bog'lanish", url="https://t.me/mrxruslann")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    builder.adjust(1) 
    
    try:
        await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Creator menyusini ochishda xatolik: {e}")

# --- 5. Baholash (Reyting) bo'limi ---
@router.callback_query(F.data == "menu_rate")
async def process_rate_menu(callback: CallbackQuery):
    await callback.answer()
    text = "⭐ <b>Botni baholash</b>\n\nBaza o'chirilgani uchun reyting funksiyasi ishlamaydi."
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    
    try:
        await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        logging.error(f"Reyting menyusini ochishda xatolik: {e}")
