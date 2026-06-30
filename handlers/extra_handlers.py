import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db
from utils.aladhan_api import get_prayer_times

router = Router()

# --- 1. Avtomatik eslatma tekshiruvi ---
async def check_and_send_reminders():
    # Bu funksiya scheduler tomonidan chaqiriladi
    pass 

# --- 2. Eslatma sozlamalari ---
@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    await callback.answer()
    text = "🔔 <b>Eslatma sozlamalari</b>\n\nBu funksiya ustida ishlar olib borilmoqda."
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    
    await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")

# --- 3. Mazhab sozlamalari ---
@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    await callback.answer()
    
    # Bazadan foydalanuvchining joriy sozlamasini olamiz (agar kiritilgan bo'lsa)
    user_id = callback.from_user.id
    user_data = db.get_user_data(user_id)
    school = user_data[4] if user_data else 0 # 0 - Hanafi, 1 - Shafi'i
    
    status = "Hanafi" if school == 0 else "Shafi'i"
    
    text = f"⚙️ <b>Sozlamalar</b>\n\nJoriy mazhabingiz: <b>{status}</b>"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🕌 Hanafi", callback_data="set_school_0")
    builder.button(text="🕋 Shafi'i", callback_data="set_school_1")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    builder.adjust(1)

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("set_school_"))
async def set_school(callback: CallbackQuery):
    school = int(callback.data.split("_")[-1])
    db.update_school(callback.from_user.id, school)
    await callback.answer("✅ Mazhab saqlandi!")
    # Sozlamalar menyusini yangilash uchun qayta chaqiramiz
    await process_settings(callback)

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

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")

# --- 5. Baholash (Reyting) bo'limi ---
@router.callback_query(F.data == "menu_rate")
async def process_rate_menu(callback: CallbackQuery):
    await callback.answer()
    avg, count = db.get_rating_stats()
    text = f"⭐ <b>Botni baholash</b>\n\nJoriy reyting: <b>{avg}</b> ({count} ta ovoz)"
    
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(text=str(i), callback_data=f"rate_{i}")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")
    builder.adjust(5, 1)

    await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("rate_"))
async def process_rate(callback: CallbackQuery):
    rating = int(callback.data.split("_")[1])
    db.update_rating(callback.from_user.id, rating)
    await callback.answer("⭐ Baholaganingiz uchun tashakkur!")
    await process_rate_menu(callback)
