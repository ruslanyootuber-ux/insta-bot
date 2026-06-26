from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.duo_data import DUOLAR
from keyboards.duo_kb import get_duo_categories_kb, get_duo_list_kb, get_duo_text_kb

router = Router()

# 1. Duolar menyusi (Kategoriyalarni ko'rsatadi)
@router.callback_query(F.data == "menu_duo")
async def show_duo_categories(callback: CallbackQuery):
    await callback.message.edit_text("🤲 <b>Duolar bo'limi</b>\n\nMarhamat, kerakli mavzuni tanlang:", 
                                     reply_markup=get_duo_categories_kb())

# 2. Tanlangan kategoriyadagi duolar ro'yxati
@router.callback_query(F.data.startswith("cat_"))
async def show_duo_list(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    await callback.message.edit_text(f"📖 <b>{category.capitalize()} duolari:</b>", 
                                     reply_markup=get_duo_list_kb(category))

# 3. Tanlangan duoning matnini ko'rsatish
@router.callback_query(F.data.startswith("showduo_"))
async def show_duo_text(callback: CallbackQuery):
    # data format: showduo_kategoriya_index
    parts = callback.data.split("_")
    cat = parts[1]
    idx = int(parts[2])
    
    duo = DUOLAR[cat][idx]
    
    text = (f"🤲 <b>{duo['title']}</b>\n\n"
            f"🇸🇦 <i>{duo['ar']}</i>\n\n"
            f"🇺🇿 <b>Ma'nosi:</b> {duo['uz']}")
    
    await callback.message.edit_text(text, reply_markup=get_duo_text_kb(cat, idx))