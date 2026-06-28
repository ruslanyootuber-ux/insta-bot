# handlers/tasbeeh_handlers.py (ёки тегишли файл)

from aiogram import Router, F
from aiogram.types import CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "menu_tasbeeh") # "menu_tasbeeh" ўрнига ўзингиздаги callback'ни қўйинг
async def process_tasbeeh(callback: CallbackQuery):
    await callback.answer()

    builder = InlineKeyboardBuilder()

    # Тасбеҳ иловасини очиш (Линкнинг охирига tasbeeh.html қўшилди)
    builder.button(
        text="📿 ✨ SMART TASBEEH ОЧИШ ✨ 📿", 
        web_app=WebAppInfo(url="https://ruslanyootuber-ux.github.io/insta-bot/tasbeeh.html") 
    )
    builder.button(text="⬅️ Асосий Меню", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "⚡ <b>⚜️ ULTRA PREMIUM SMART TASBEEH ⚜️</b> ⚡\n"
        "───────────────────────────────\n\n"
        "📿 <b>Рақамли ақлли тасбеҳга хуш келибсиз!</b>\n\n"
        "Қуйидаги тугмани босиш орқали бот ичида замонавий, хотирага эга ва "
        "визуал эффектларга бой тасбеҳни ишга туширинг.\n\n"
        "<b>💎 Илова имкониятлари:</b>\n"
        "┌ 🔄 <i>Автоматик 33/66/99 зикр алмашинуви</i>\n"
        "├ 💾 <i>Саноқни қурилма хотирасида сақлаш</i>\n"
        "├ 📳 <i>Ҳар 33 тада Smart Haptic вибрация ва товуш</i>\n"
        "└ 🌙 <i>Кўзни толиқтирмас Dark Glassmorphism дизайн</i>\n\n"
        "───────────────────────────────"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
