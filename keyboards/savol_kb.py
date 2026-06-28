from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.data_savol_javob import SAVOL_JAVOBLAR

def get_savol_menu_kb(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    items_per_page = 5  # Har bir sahifada 5 ta savol
    
    start = page * items_per_page
    end = start + items_per_page
    
    # 1. Sahifa bo'yicha savollarni tugmaga aylantirish
    for i in range(start, min(end, len(SAVOL_JAVOBLAR))):
        # Tugma matni: Savol raqami va qisqa mazmuni
        text = f"{i + 1}. {SAVOL_JAVOBLAR[i]['savol'][:25]}..."
        builder.button(text=text, callback_data=f"faq_ans_{i}")
    
    # 2. Navigatsiya tugmalari (Oldinga/Orqaga)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"faq_page_{page-1}"))
    if end < len(SAVOL_JAVOBLAR):
        nav_buttons.append(InlineKeyboardButton(text="Oldinga ➡️", callback_data=f"faq_page_{page+1}"))
    
    # Navigatsiya tugmalarini qatorga qo'shish
    if nav_buttons:
        builder.row(*nav_buttons)
        
    # 3. Asosiy menyuga qaytish
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyuga", callback_data="back_to_main"))
    
    builder.adjust(1) # Har bir tugma alohida qatorda
    return builder.as_markup()
