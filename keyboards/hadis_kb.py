from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_hadis_keyboard(index: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇸🇦 Arabcha", callback_data=f"h_ar_{index}")
    builder.button(text="🇺🇿 Lotin", callback_data=f"h_lat_{index}")
    builder.button(text="🇷🇺 Kirill", callback_data=f"h_kir_{index}")
    builder.row(builder.button(text="🔄 Yangi hadis", callback_data="menu_hadis"))
    builder.row(builder.button(text="⬅️ Asosiy menyu", callback_data="back_to_menu"))
    builder.adjust(3, 1, 1)
    return builder.as_markup()