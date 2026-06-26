from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from data.duo_data import DUOLAR

def get_duo_categories_kb():
    builder = InlineKeyboardBuilder()
    for cat in DUOLAR.keys():
        builder.button(text=cat.capitalize(), callback_data=f"cat_{cat}")
    builder.row(InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_menu"))
    builder.adjust(2)
    return builder.as_markup()

def get_duo_list_kb(cat):
    builder = InlineKeyboardBuilder()
    for i, duo in enumerate(DUOLAR[cat]):
        builder.button(text=f"{i+1}", callback_data=f"showduo_{cat}_{i}")
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu_duo"))
    builder.adjust(5)
    return builder.as_markup()

def get_duo_text_kb(cat, idx):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Ro'yxatga qaytish", callback_data=f"cat_{cat}"))
    return builder.as_markup()