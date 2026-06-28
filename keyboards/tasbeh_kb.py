from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from data.tasbeh_data import TASBEH_ZIKRLARI # Fayl nomi tasbeh_data bo'lishi shart

def get_tasbeh_keyboard(count: int, index: int):
    builder = InlineKeyboardBuilder()
    
    # TASBEH_ZIKRLARI ro'yxatidan foydalanamiz
    builder.row(InlineKeyboardButton(text=f"📿 {TASBEH_ZIKRLARI[index]['name']}", callback_data="change_zikr"))
    builder.row(InlineKeyboardButton(text=f"🔢 {count}", callback_data="count_tasbeh"))
    builder.row(
        InlineKeyboardButton(text="🔄 Nollash", callback_data="reset_tasbeh"),
        InlineKeyboardButton(text="⬅️ Menyu", callback_data="back_to_main")
    )
    
    return builder.as_markup()