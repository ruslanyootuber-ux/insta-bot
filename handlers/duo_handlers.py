from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.duo_data import DUOLAR # Hadis kabi to'g'ridan-to'g'ri import

router = Router()

# Menyu uchun tugmalar (Hadisdagi kabi)
@router.callback_query(F.data == "menu_duo")
async def show_duo_categories(callback: CallbackQuery):
    # Bu yerda kategoriyalarni tanlash tugmalarini chiqarasiz
    await callback.message.edit_text("Kerakli duo turini tanlang:", reply_markup=...) 

@router.callback_query(F.data.startswith("duo_"))
async def show_duo_content(callback: CallbackQuery):
    await callback.answer()
    
    # Callback format: duo_kategoriya_index
    data = callback.data.split("_")
    category = data[1]
    index = int(data[2])
    
    duo = DUOLAR[category][index]
    
    text = (f"🤲 <b>{duo['title']}</b>\n\n"
            f"🇸🇦 <i>{duo['arabic']}</i>\n\n"
            f"🇺🇿 <b>Ma'nosi:</b> {duo['uzbek']}")
    
    await callback.message.edit_text(text, reply_markup=...) # Tugmalarni o'zingiz qo'shasiz