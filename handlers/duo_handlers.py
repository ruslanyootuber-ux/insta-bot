from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.duo_data import DUOLAR
from keyboards.duo_kb import get_duo_menu_keyboard

router = Router()

# 1. Menyu tugmasi uchun alohida handler
@router.callback_query(F.data == "menu_duo")
async def show_duo_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📖 <b>Duo bo‘limiga xush kelibsiz!</b>\nKerakli kategoriyani tanlang:", 
        reply_markup=get_duo_menu_keyboard()
    )

# 2. Kategoriyalar uchun handler (menu_duo dan farqli ekanini tekshiramiz)
@router.callback_query(F.data.startswith("duo_") & (F.data != "menu_duo"))
async def show_duo_content(callback: CallbackQuery):
    # duo_tong yoki duo_kech kabi keladi
    category = callback.data.split("_")[1]
    
    # Kategoriya borligini tekshiramiz
    if category in DUOLAR:
        duo = DUOLAR[category][0] 
        text = (
            f"🤲 <b>{duo['title']}</b>\n\n"
            f"🇸🇦 <i>{duo['ar']}</i>\n\n"
            f"📝 <b>O‘qilishi:</b>\n{duo['lat']}\n\n"
            f"🇺🇿 <b>Ma'nosi:</b>\n{duo['uz']}"
        )
        await callback.message.edit_text(text, reply_markup=get_duo_menu_keyboard())
    else:
        await callback.answer("Hozircha bu kategoriya bo'sh.")