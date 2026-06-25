from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.inline_kb import get_regions_keyboard
from loader import db  # Bazani import qilamiz

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Foydalanuvchini bazaga qo'shish
    db.add_user(message.from_user.id, message.from_user.full_name)
    
    text = (
        "🕌 <b>Assalomu alaykum!</b>\n\n"
        "Xush kelibsiz! O'zingizga kerakli viloyatni tanlang:"
    )
    await message.answer(text, reply_markup=get_regions_keyboard())
