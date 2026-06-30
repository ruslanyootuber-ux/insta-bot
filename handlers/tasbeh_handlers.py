# handlers/tasbeh_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "menu_tasbeh")
async def process_tasbeh(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    
    # Premium WebApp tugmasi
    builder.button(
        text="📿 PREMIUM TASBEHNI OCHISH", 
        web_app=WebAppInfo(url="https://ruslanyootuber-ux.github.io/insta-bot/tasbeh.html") 
    )
    # Orqaga qaytish tugmasi
    builder.button(
        text="⬅️ ORQAGA", 
        callback_data="back_to_main"
    )
    builder.adjust(1)

    text = (
        "✨ <b>Premium Islomiy Tasbeh</b> ✨\n\n"
        "Ruhoniy xotirjamlik va zikrlar darsi uchun maxsus yaratilgan inline ilova.\n\n"
        "🟢 <b>Imkoniyatlari:</b>\n"
        "• Haqiqiy qurilma tebranishi (Haptic Feedback)\n"
        "• Chiroyli iOS & Android UI-dizayni\n"
        "• Har 33 talikda avtomatik almashuvchi zikrlar"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
