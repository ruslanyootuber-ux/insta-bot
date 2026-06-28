from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_taxorat_step_kb(current_step: int, total_steps: int, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Tilga qarab tugma nomlarini belgilaymiz
    next_text = "Keyingi ➡️" if lang == 'latin' else "Кейинги ➡️"
    prev_text = "⬅️ Oldingi" if lang == 'latin' else "⬅️ Олдинги"
    menu_text = "🏠 Asosiy menyu" if lang == 'latin' else "🏠 Асосий меню"

    # Oldingi qadam tugmasi (agar 1-qadamda bo'lmasak)
    if current_step > 0:
        builder.button(text=prev_text, callback_data=f"taxorat_{current_step - 1}_{lang}")
    
    # Keyingi qadam tugmasi (agar oxirgi qadamda bo'lmasak)
    if current_step < total_steps - 1:
        builder.button(text=next_text, callback_data=f"taxorat_{current_step + 1}_{lang}")
        
    # Asosiy menyuga qaytish
    builder.button(text=menu_text, callback_data=f"main_menu_{lang}")
    
    # Tugmalarni joylashtirish (2 tasi yonma-yon, menyu pastda)
    builder.adjust(2, 1)
    return builder.as_markup()