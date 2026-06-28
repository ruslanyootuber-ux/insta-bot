# keyboards/suralar_kb.py

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_suralar_list_kb(suralar_list: list) -> InlineKeyboardMarkup:
    """Суралар рўйхати учун тугмалар генератори"""
    builder = InlineKeyboardBuilder()
    
    for sura in suralar_list:
        builder.button(text=sura["name"], callback_data=f"sura_view_{sura['id']}")
        
    builder.button(text="⬅️ Асосий меню", callback_data="back_to_main")
    builder.adjust(1)  # Ҳар бир қаторда 1 тадан сура тугмаси жойлашади
    return builder.as_markup()

def get_sura_back_kb() -> InlineKeyboardMarkup:
    """Сура ичидан орқага қайтиш тугмалари"""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Суралар рўйхатига қайтиш", callback_data="suralar")
    builder.button(text="🏠 Асосий меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()
