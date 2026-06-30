# handlers/start.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

# Inline tugmalarni import qilamiz
from keyboards.inline_kb import get_main_menu_kb, get_regions_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    # Premium ko'rinishdagi xush kelibsiz matni
    text = (
        "<b>Assalomu alaykum, foydalanuvchi!</b> 👋\n\n"
        "«Namoz Taqvim» ilmiy-ma'rifiy botiga xush kelibsiz.\n"
        "Biz sizga kundalik ibodatlaringizni oson va tartibli bajarishda ko'maklashamiz.\n\n"
        "┌───────────────\n"
        "├ 🕌 Aniq namoz vaqtlari\n"
        "├ 🕋 Qibla yo'nalishi (Jonli)\n"
        "├ 📿 Zikr va Tasbehlar\n"
        "└───────────────\n\n"
        "<i>Quyidagi menyudan kerakli bo'limni tanlang:</i>"
    )
    
    await message.answer(
        text=text, 
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    text = (
        "<b>Bosh menyu</b>\n\n"
        "<i>Kerakli bo'limni tanlang:</i>"
    )
    await callback.message.edit_text(
        text=text, 
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "menu_regions")
async def show_regions(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📍 Hududni tanlang:</b>", 
        reply_markup=get_regions_keyboard(),
        parse_mode="HTML"
    )
