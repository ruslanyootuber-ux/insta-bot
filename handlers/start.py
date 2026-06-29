from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

# Baza va klaviaturalar importi
from statistika_data import add_user
from keyboards.inline_kb import get_main_menu_kb, get_regions_keyboard

router = Router()

# Botni ishga tushirganda chiqadigan asosiy menyu
@router.message(Command("start"))
async def start_handler(message: Message):
    # Foydalanuvchini bazaga qo'shamiz
    add_user(message.from_user.id)
    
    await message.answer(
        "Assalomu alaykum! Kerakli bo'limni tanlang 👇", 
        reply_markup=get_main_menu_kb()
    )

# "Namoz vaqtlari" ni bosganda viloyatlar chiqishi
@router.callback_query(F.data == "menu_regions")
async def show_regions(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Viloyatni tanlang:", 
        reply_markup=get_regions_keyboard()
    )
