from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from keyboards.inline_kb import get_main_menu_kb, get_regions_keyboard
from utils.aladhan_api import get_prayer_times
from loader import db 

router = Router()

async def get_live_prayer_text(user_id):
    # Bazadan hududni olamiz (default "Toshkent")
    region = db.get_district(user_id) 

    times = await get_prayer_times(region)
    if times and "next_prayer" in times:
        return f"⏰ Navbatdagi: <b>{times['next_prayer']}</b>"
    return "⏰ Namoz vaqtlari yuklanmoqda..."

@router.message(Command("start"))
async def start_handler(message: Message):
    # Foydalanuvchini bazaga qo'shamiz
    db.add_user(message.from_user.id, message.from_user.full_name)

    live_info = await get_live_prayer_text(message.from_user.id)

    text = (
        f"<b>Assalomu alaykum, {message.from_user.full_name}!</b> 👋\n\n"
        f"«Namoz Taqvim» ilmiy-ma'rifiy botiga xush kelibsiz.\n\n"
        f"┌───────────────\n"
        f"├ {live_info}\n"
        f"├ 🕋 Qibla yo'nalishi (Live)\n"
        f"└───────────────\n\n"
        f"<i>Quyidagi menyudan kerakli bo'limni tanlang:</i>"
    )

    await message.answer(
        text=text, 
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    live_info = await get_live_prayer_text(callback.from_user.id)

    text = (
        f"<b>Bosh menyu</b>\n\n"
        f"<i>{live_info}</i>\n\n"
        f"<i>Kerakli bo'limni tanlang:</i>"
    )

    try:
        await callback.message.edit_text(
            text=text, 
            reply_markup=get_main_menu_kb(),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text=text, 
            reply_markup=get_main_menu_kb(),
            parse_mode="HTML"
        )
    await callback.answer()

@router.callback_query(F.data == "menu_regions")
async def show_regions(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📍 Hududni tanlang:</b>", 
        reply_markup=get_regions_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()
