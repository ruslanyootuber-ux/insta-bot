from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

# Zikrlar asosiy menyusi
def get_zikr_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌅 Tonggi zikrlar", callback_data="zikr_start_morning")
    builder.button(text="🌇 Kechki zikrlar", callback_data="zikr_start_evening")
    builder.button(text="⬅️ Asosiy menyuga qaytish", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

# Varaqlash (Oldingi/Keyingi) tugmalari
def get_zikr_pagination_keyboard(z_type: str, current_index: int, total: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # ⬅️ Oldinga tugmasi
    if current_index > 0:
        builder.button(text="⬅️", callback_data=f"zikr_{z_type}_{current_index - 1}")
    else:
        builder.button(text="⏹", callback_data="ignore") # Boshiga yetganda bosilmaydi
        
    # O'rtadagi raqam (masalan, 1/10)
    builder.button(text=f"{current_index + 1} / {total}", callback_data="ignore")
    
    # ➡️ Keyingisi tugmasi
    if current_index < total - 1:
        builder.button(text="➡️", callback_data=f"zikr_{z_type}_{current_index + 1}")
    else:
        builder.button(text="⏹", callback_data="ignore") # Oxiriga yetganda
        
    builder.button(text="🔙 Zikrlar menyusi", callback_data="menu_zikr_main")
    builder.adjust(3, 1) # Tepadagi 3 ta tugma bir qatorda, pastdagi alohida
    return builder.as_markup()