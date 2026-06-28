from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from transliterate import translit
from data.data_savol_javob import SAVOL_JAVOBLAR
# Klaviaturalarni bitta joydan chaqiring (inline_kb.py yoki savol_kb.py)
from keyboards.inline_kb import get_faq_menu_kb 
from database import get_language, set_language
from cyrtranslit import to_cyrillic

router = Router()

# 1. Savollar ro'yxatini ko'rsatish
@router.callback_query(F.data.startswith("faq_page_"))
async def show_faq_list(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_text("Kerakli savolni tanlang:", reply_markup=get_faq_menu_kb(page))

# 2. Savol javobini ko'rsatish
@router.callback_query(F.data.startswith("faq_ans_"))
async def show_faq_answer(callback: CallbackQuery):
    index = int(callback.data.split("_")[2])
    item = SAVOL_JAVOBLAR[index]
    
    user_lang = get_language(callback.from_user.id)
    savol = item['savol']
    javob = item['javob']
    
    if user_lang == "cyrillic":
    # 'ru' parametri orqali kirillchaga o'girish (uzbek tili uchun ham ishlaydi)
    savol = translit(savol, 'ru')
    javob = translit(javob, 'ru')
        
    text = f"❓ <b>{savol}</b>\n\n<blockquote>{javob}</blockquote>"
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data="faq_page_0")
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())

# 3. Tilni almashtirish
@router.callback_query(F.data.startswith("lang_"))
async def change_lang(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_language(callback.from_user.id, lang)
    msg = "Til o'zgartirildi!" if lang == "latin" else "Тил ўзгартирилди!"
    await callback.answer(msg, show_alert=True)
