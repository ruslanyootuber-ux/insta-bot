from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from data.zikr_data import ZIKRLAR

def get_tasbeh_keyboard(count: int, zikr_index: int):
    builder = InlineKeyboardBuilder()
    
    # 1. Katta va ko'zga tashlanadigan sanoq tugmasi
    builder.row(InlineKeyboardButton(text=f"📿 BOSISH: {count}", callback_data="count_zikr"))
    
    # 2. Boshqaruv qatori
    builder.row(
        InlineKeyboardButton(text="🔄 Nollash", callback_data="reset_zikr"),
        InlineKeyboardButton(text="⬅️ Menyu", callback_data="back_to_menu")
    )
    
    return builder.as_markup()