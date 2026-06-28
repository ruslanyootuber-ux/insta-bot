# handlers/qibla_handlers.py ичидаги тегишли қисми

from aiogram import Router, F
from aiogram.types import CallbackQuery, WebAppInfo # <-- WebAppInfo қўшилди
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "menu_qibla")
async def process_qibla(callback: CallbackQuery):
    await callback.answer()
    
    builder = InlineKeyboardBuilder()
    
    # Жонли компас очиш тугмаси (Ҳавола жойига ўз сайтингизни қўясиз)
    builder.button(
        text="🧭 Жонли Компасни очиш", 
        web_app=WebAppInfo(url="ruslanyootuber-ux.github.io") 
    )
    builder.button(text="⬅️ Асосий меню", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "🕋 <b>Реал вақтдаги Қибла Компаси</b>\n\n"
        "Пастдаги тугмани босиш орқали бот ичида жонли, ҳаракатланадиган "
        "рақамли компасни ишга туширишингиз мумкин.\n\n"
        "<i>📱 Бунинг учун телефонингизда йўналиш датчиклари тўғри ишлаши керак.</i>"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )