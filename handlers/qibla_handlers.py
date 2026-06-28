# handlers/qibla_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "menu_qibla")
async def process_qibla(callback: CallbackQuery):
    await callback.answer()

    builder = InlineKeyboardBuilder()

    # Жонли компас очиш ва орқага қайтиш тугмалари
    builder.button(
        text="✨ 🧭 ЖОНЛИ КОМПАСНИ ОЧИШ 🧭 ✨", 
        web_app=WebAppInfo(url="https://ruslanyootuber-ux.github.io/insta-bot/") 
    )
    builder.button(text="⬅️ Асосий Менюга Қайтиш", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "⚡ <b>⚜️ ULTRA PREMIUM QIBLA COMPASS ⚜️</b> ⚡\n"
        "───────────────────────────────\n\n"
        "🕋 <b>Реал вақт режимидаги рақамли Қибла компасига хуш келибсиз!</b>\n\n"
        "Пастдаги махсус тугмани босиш орқали бот ичида жонли, телефон "
        "гироскопи ва магнит датчиклари билан реал вақтда (Live) ҳаракатланувчи "
        "интерактив компасни ишга туширасиз.\n\n"
        "<b>📐 Компас имкониятлари:</b>\n"
        "┌ 🎯 <i>0.15° аниқликдаги Low-pass фильтр тизими</i>\n"
        "├ 🛡️ <i>Premium Luxury дизайн ва тунги режим (AMOLED)</i>\n"
        "└ 📳 <i>Тўғри йўналишда автоматик Haptic (вибрация)</i>\n\n"
        "───────────────────────────────\n"
        "<i>📱 Эслатма: Мукаммал ишлаши учун телефонингизда йўналиш датчиклари (Compass/Gyroscope) фаол бўлиши шарт.</i>"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
