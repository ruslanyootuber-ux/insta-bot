from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.inline_kb import get_regions_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    print("LOG: /start komandasi muvaffaqiyatli ushlandi!") # Terminalda ko'rish uchun
    text = (
        "🕌 <b>Assalomu alaykum!</b>\n\n"
        "O'zingizga kerakli viloyatni tanlang:"
    )
    await message.answer(text, reply_markup=get_regions_keyboard())
