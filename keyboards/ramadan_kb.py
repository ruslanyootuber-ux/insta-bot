# keyboards/ramadan_kb.py

from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_ramadan_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Bugungi vaqtlar", callback_data="ramadan_today")
    builder.button(text="🤲 Saharlik va Iftorlik duolari", callback_data="ramadan_duas")
    
    # callback_data айнан "back_to_main" га ўзгартирилди:
    builder.button(text="⬅️ Asosiy menyuga", callback_data="back_to_main") 
    
    builder.adjust(1)
    return builder.as_markup()
