import sys
import os

# Ushbu 2 qator Python'ga loyihaning ildiz papkasini (root) ko'rsatadi.
# Bu bilan duo_data fayli qayerda bo'lsa ham (main.py bilan birga), uni topadi.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# Endi bu import xatosiz ishlaydi
from duo_data import DUOLAR 

router = Router()

def get_duo_navigation(category, index, total):
    builder = InlineKeyboardBuilder()

    prev_index = index - 1 if index > 0 else total - 1
    next_index = index + 1 if index < total - 1 else 0

    if total > 1:
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=f"duo_{category}_{prev_index}"),
            InlineKeyboardButton(text="➡️", callback_data=f"duo_{category}_{next_index}")
        )

    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu_duo"))
    return builder.as_markup()

@router.callback_query(F.data.startswith("duo_"))
async def show_duo_content(callback: CallbackQuery):
    data = callback.data.split("_")
    
    if len(data) < 3:
        return
        
    category = data[1]
    try:
        index = int(data[2])
    except ValueError:
        index = 0

    duo_list = DUOLAR.get(category, [])
    if not duo_list:
        await callback.answer("Duolar topilmadi.", show_alert=True)
        return

    duo = duo_list[index]

    text = (f"🤲 <b>{duo['title']} ({index+1}/{len(duo_list)})</b>\n\n"
            f"🇸🇦 <i>{duo['ar']}</i>\n\n"
            f"📝 <b>O‘qilishi:</b>\n<code>{duo['lat']}</code>\n\n"
            f"🇺🇿 <b>Ma'nosi:</b>\n{duo['uz']}")

    await callback.message.edit_text(text, reply_markup=get_duo_navigation(category, index, len(duo_list)), parse_mode="HTML")
