from data.data_savol_javob import SAVOL_JAVOBLAR

@router.callback_query(F.data.startswith("faq_page_"))
async def faq_pagination_handler(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_text(
        "Quyidagi mavzulardan birini tanlang:",
        reply_markup=get_savol_menu_kb(page)
    )
