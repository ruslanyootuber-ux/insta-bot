from aiogram import Router, F
from aiogram.types import CallbackQuery
from loader import bot, db
from utils.aladhan_api import get_prayer_times

router = Router()

# --- Avtomatik eslatma funksiyasi (Scheduler uchun) ---
async def send_daily_reminders():
    users = db.get_all_users()
    for user in users:
        # user[0] = user_id, user[2] = district
        user_id, district = user[0], user[2]
        if district:
            times = await get_prayer_times(district)
            if times:
                await bot.send_message(user_id, f"🕌 <b>{district}</b> uchun yangi kun boshlandi. Namoz vaqtlarini tekshirib oling!")

# --- Menu tugmalari uchun handlerlar ---

@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    text = (
        "🔔 <b>Bildirishnoma va Eslatmalar</b>\n\n"
        "Bu bo'lim orqali siz har bir namoz vaqti kirishidan 15 yoki 30 daqiqa oldin "
        "ogohlantiruvchi xabar olishingiz mumkin.\n\n"
        "<i>⚠️ Eslatma tizimi (Scheduler) ustida ish olib borilmoqda, keyingi yangilanishda faollashadi!</i>"
    )
    await callback.answer() 
    await callback.message.answer(text)

@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    text = (
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Bunga tilni o'zgartirish, vaqt mintaqasi va Hanafi/Shafi'i mazhabini "
        "tanlash funksiyalari qo'shiladi."
    )
    await callback.answer()
    await callback.message.answer(text)

@router.callback_query(F.data == "menu_creator")
async def process_creator(callback: CallbackQuery):
    text = (
        "👨‍💻 <b>Bot Yaratuvchisi</b>\n\n"
        "Ushbu zamonaviy bot <b>Python</b> va <b>Aiogram 3.x</b> texnologiyalari "
        "asosida yaratildi.\n\n"
        "Taklif va murojaatlar uchun admin bilan bog'laning: @mrxruslann"
    )
    await callback.answer()
    await callback.message.answer(text)

@router.callback_query(F.data == "menu_rate")
async def process_rate(callback: CallbackQuery):
    await callback.answer(
        text="⭐ Botimiz sizga manzur kelganidan xursandmiz! Iltimos, do'stlaringizga ham ulashing.", 
        show_alert=True
    )