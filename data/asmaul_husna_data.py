from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.asmaul_kb import get_asmaul_keyboard
from data.asmaul_husna_data import ASMAUL_HUSNA

router = Router()

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