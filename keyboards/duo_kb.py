from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_duo_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🌅 Tonggi duolar", callback_data="duo_tong"))
    builder.row(InlineKeyboardButton(text="🌃 Kechki duolar", callback_data="duo_kech"))
    builder.row(InlineKeyboardButton(text="🚗 Safar duolari", callback_data="duo_safar"))
    builder.row(InlineKeyboardButton(text="😴 Uyqu duolari", callback_data="duo_uyqu"))
    builder.row(InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu"))
    return builder.as_markup()