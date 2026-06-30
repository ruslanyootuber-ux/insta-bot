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
        text="📿 TASBEHNI OCHISH", 
        web_app=WebAppInfo(url="https://ruslanyootuber-ux.github.io/insta-bot/tasbeh.html") 
    )
    # Orqaga qaytish tugmasi
    builder.button(
        text="⬅️ ORQAGA", 
        callback_data="back_to_main"
    )
    builder.adjust(1)

    text = (
    "✨ <b>Islomiy Tasbeh</b> ✨\n\n"
    "Qalblar halovati va Allohning zikri ila munavvar bo'lishi uchun maxsus tayyorlangan raqamli tasbeh.\n\n"
    "🪄 <b>Imkoniyatlari:</b>\n"
    "• Haqiqiy tasbeh hissini beruvchi mayin tebranish\n"
    "• Ko'zlarni charchatmaydigan va ko'ngilga xotirjamlik bag'ishlovchi Premium dizayn\n"
    "• Har 33 ta zikrda avtomatik ravishda yangilanadigan tasbeh duolari"
)


    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
