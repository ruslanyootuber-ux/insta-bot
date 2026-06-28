from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from data.asmaul_husna_data import ASMAUL_HUSNA

router = Router()

# Klaviatura funksiyasini shu yerning o'ziga joylashtirdik (import qilib o'tirmaymiz)
def get_asmaul_keyboard(index: int, total: int):
    builder = InlineKeyboardBuilder()
    prev_index = index - 1 if index > 0 else total - 1
    next_index = index + 1 if index < total - 1 else 0
    builder.row(
        InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"asma_{prev_index}"),
        InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"asma_{next_index}")
    )
    builder.row(InlineKeyboardButton(text="⬅️ Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()

async def send_asmaul_page(callback: CallbackQuery, index: int):
    item = ASMAUL_HUSNA[index]
    text = (
        f"✨ <b>Asmaul Husna: {index + 1}-ism</b>\n\n"
        f"🇸🇦 Arabcha: <b>{item['ar']}</b>\n"
        f"🇺🇿 Lotincha: <b>{item['lat']}</b>\n\n"
        f"📖 Ma'nosi: <i>{item['uz']}</i>"
    )
    await callback.message.edit_text(
        text, 
        reply_markup=get_asmaul_keyboard(index, len(ASMAUL_HUSNA))
    )
    await callback.answer()

@router.callback_query(F.data == "menu_asmaul")
async def show_asmaul(callback: CallbackQuery):
    await send_asmaul_page(callback, 0)

@router.callback_query(F.data.startswith("asma_"))
async def navigation_asmaul(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    await send_asmaul_page(callback, index)