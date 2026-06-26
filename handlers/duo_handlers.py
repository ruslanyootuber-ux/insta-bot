@router.callback_query(F.data.startswith("duo_"))
async def show_duo_content(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    duo = DUOLAR.get(category, [])[0] # Birinchi duoni olish
    
    text = (
        f"🤲 <b>{duo['title']}</b>\n\n"
        f"🇸🇦 <i>{duo['ar']}</i>\n\n"
        f"📝 <b>O‘qilishi:</b>\n{duo['lat']}\n\n"
        f"🇺🇿 <b>Ma'nosi:</b>\n{duo['uz']}"
    )
    
    await callback.message.edit_text(text, reply_markup=get_duo_menu_keyboard())