# keyboards/erkaklar_namozi_kb.py

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_erkaklar_namozi_step_kb(current_step: int, total_steps: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    next_text = "Кейинги ➡️"
    prev_text = "⬅️ Олдинги"
    menu_text = "🏠 Асосий меню"

    if current_step > 0:
        builder.button(text=prev_text, callback_data=f"erkaklar_namozi_{current_step - 1}")
    
    if current_step < total_steps - 1:
        builder.button(text=next_text, callback_data=f"erkaklar_namozi_{current_step + 1}")
        
    builder.button(text=menu_text, callback_data="back_to_main")
    
    builder.adjust(2, 1)
    return builder.as_markup()
