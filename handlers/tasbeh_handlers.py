from aiogram import Router, F
from aiogram.types import CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "menu_tasbeh")
async def process_tasbeh(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📿 PREMIUM TASBEHNI OCHISH", 
        web_app=WebAppInfo(url="https://ruslanyootuber-ux.github.io/insta-bot/tasbeh.html") 
    )
    builder.button(text="⬅️ ORQAGA", callback_data="back_to_main")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "✨ <b>Premium Islomiy Tasbeh</b> ✨\n\n"
        "Ruhoniy xotirjamlik uchun maxsus yaratilgan.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
