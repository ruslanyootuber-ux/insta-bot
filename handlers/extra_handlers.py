from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    text = (
        "🔔 <b>Bildirishnoma va Eslatmalar</b>\n\n"
        "Bu bo'lim orqali siz har bir namoz vaqti kirishidan 15 yoki 30 daqiqa oldin "
        "ogohlantiruvchi xabar olishingiz mumkin.\n\n"
        "<i>⚠️ Eslatma tizimi (Scheduler) ustida ish olib borilmoqda, keyingi yangilanishda faollashadi!</i>"
    )
    # Callbackni yopamiz (tepadagi yuklanyapti... yozuvi ketishi uchun)
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
        "Taklif va murojaatlar uchun admin bilan bog'laning: @mrxruslann" # O'zingizning userneyamingizni yozing
    )
    await callback.answer()
    await callback.message.answer(text)

@router.callback_query(F.data == "menu_rate")
async def process_rate(callback: CallbackQuery):
    # Ekranga qalqib chiquvchi oyna (Alert) ko'rsatamiz
    await callback.answer(
        text="⭐ Botimiz sizga manzur kelganidan xursandmiz! Iltimos, do'stlaringizga ham ulashing.", 
        show_alert=True
    )