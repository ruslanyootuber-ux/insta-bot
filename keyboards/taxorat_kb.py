from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_taxorat_step_kb(current_step: int, total_steps: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Фақат кириллча тугма номлари
    next_text = "Кейинги ➡️"
    prev_text = "⬅️ Олдинги"
    menu_text = "🏠 Асосий меню"

    if current_step > 0:
        builder.button(text=prev_text, callback_data=f"taxorat_{current_step - 1}")
    
    if current_step < total_steps - 1:
        builder.button(text=next_text, callback_data=f"taxorat_{current_step + 1}")
        
    builder.button(text=menu_text, callback_data="back_to_main") # Сиздаги бош менюга қайтиш калити
    
    builder.adjust(2, 1)
    return builder.as_markup()