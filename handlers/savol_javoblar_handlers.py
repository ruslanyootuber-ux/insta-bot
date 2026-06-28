from transliterate import to_cyrillic
from aiogram import types, F
from data import SAVOL_JAVOBLAR

# Foydalanuvchi tanlovi (buni bazada yoki user_data da saqlashingiz kerak)
# Hozircha misol uchun:
user_lang = "cyrillic" # yoki "latin"

async def show_faq_answer(callback: types.CallbackQuery, faq_index: int):
    item = SAVOL_JAVOBLAR[faq_index]
    
    savol = item['savol']
    javob = item['javob']
    
    # Agar foydalanuvchi Kirillcha tanlagan bo'lsa
    if user_lang == "cyrillic":
        savol = to_cyrillic(savol)
        javob = to_cyrillic(javob)
        
    # Tsitata (blockquote) formatida yuborish
    text = f"❓ <b>{savol}</b>\n\n<blockquote>{javob}</blockquote>"
    
    await callback.message.edit_text(text, parse_mode="HTML")
