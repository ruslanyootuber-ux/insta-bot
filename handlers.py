from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
import keyboards

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Assalomu alaykum! Zamonaviy botga xush kelibsiz.", reply_markup=keyboards.get_main_menu())

@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.edit_text("Bu bot juda mukammal ishlash uchun mo'ljallangan!", reply_markup=keyboards.get_back_menu())

@router.callback_query(F.data == "ask_question")
async def ask(callback: CallbackQuery):
    await callback.message.edit_text("Savolingizni yozing yoki menyudan tanlang:", reply_markup=keyboards.get_back_menu())

@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text("Bosh menyu:", reply_markup=keyboards.get_main_menu())
