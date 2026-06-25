from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Bot haqida", callback_data="about")],
        [InlineKeyboardButton(text="🤖 Savol berish", callback_data="ask_question")],
        [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")]
    ])
    return keyboard

def get_back_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")]
    ])
    return keyboard
