from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_ramadan_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Bugungi vaqtlar", callback_data="ramadan_today")
    builder.button(text="🤲 Saharlik va Iftorlik duolari", callback_data="ramadan_duas")
    builder.button(text="⬅️ Orqaga", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()