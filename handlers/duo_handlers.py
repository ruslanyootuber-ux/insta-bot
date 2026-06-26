from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_duo_navigation(category, index, total):
    builder = InlineKeyboardBuilder()
    
    # ⬅️ Oldingi / Keyingi tugmalari
    prev_index = index - 1 if index > 0 else total - 1
    next_index = index + 1 if index < total else 0
    
    if total > 1:
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=f"duo_{category}_{prev_index}"),
            InlineKeyboardButton(text="➡️", callback_data=f"duo_{category}_{next_index}")
        )
    
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu_duo"))
    return builder.as_markup()

@router.callback_query(F.data.startswith("duo_"))
async def show_duo_content(callback: CallbackQuery):
    data = callback.data.split("_")
    category = data[1]
    index = int(data[2]) if len(data) > 2 else 0
    
    duo_list = DUOLAR.get(category, [])
    duo = duo_list[index]
    
    text = (f"🤲 <b>{duo['title']} ({index+1}/{len(duo_list)})</b>\n\n"
            f"🇸🇦 <i>{duo['ar']}</i>\n\n"
            f"📝 <b>O‘qilishi:</b>\n{duo['lat']}\n\n"
            f"🇺🇿 <b>Ma'nosi:</b>\n{duo['uz']}")
            
    await callback.message.edit_text(text, reply_markup=get_duo_navigation(category, index, len(duo_list)))