from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_hadis_keyboard(index: int):
    builder = InlineKeyboardBuilder()
    
    # Tugmalarni alohida qo'shamiz
    builder.button(text="🇸🇦 Arabcha", callback_data=f"h_ar_{index}")
    builder.button(text="🇺🇿 Lotin", callback_data=f"h_lat_{index}")
    builder.button(text="🇷🇺 Kirill", callback_data=f"h_kir_{index}")
    
    # row() ichida builder.button() ni chaqirmang, shunchaki tugma qo'shing
    builder.row(InlineKeyboardButton(text="🔄 Yangi hadis", callback_data="menu_hadis"))
    builder.row(InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu"))
    
    builder.adjust(3, 1, 1)
    return builder.as_markup()