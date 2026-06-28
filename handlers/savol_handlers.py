from aiogram import Router, F, types
from data.data_savol_javob import SAVOL_JAVOBLAR
# get_savol_menu_kb funksiyasini keyboards papkasidan import qilamiz
from keyboards.savol_kb import get_savol_menu_kb 

router = Router()

@router.callback_query(F.data.startswith("faq_page_"))
async def faq_pagination_handler(callback: types.CallbackQuery):
    # callback dan sahifa raqamini olish
    page = int(callback.data.split("_")[2])
    
    await callback.message.edit_text(
        "Quyidagi mavzulardan birini tanlang:",
        reply_markup=get_savol_menu_kb(page)
    )

# Agar savol javobini ko'rsatuvchi handler hali yo'q bo'lsa, uni ham qo'shib qo'ying:
@router.callback_query(F.data.startswith("faq_ans_"))
async def show_faq_answer(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[2])
    item = SAVOL_JAVOBLAR[index]
    
    text = f"❓ <b>{item['savol']}</b>\n\n<blockquote>{item['javob']}</blockquote>"
    
    # Orqaga qaytish tugmasi
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data="faq_page_0")
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
