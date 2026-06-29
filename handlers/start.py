from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

# Baza va klaviaturalar importi
from data.statistika_data import add_user
from keyboards.inline_kb import get_main_menu_kb, get_regions_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    # Foydalanuvchini bazaga qo'shamiz
    # Agar foydalanuvchi bazada bo'lsa, hech narsa qilmaydi (INSERT OR IGNORE)
    add_user(message.from_user.id)
    
    # Rasmli yoki chiroyli xabar yuborish uchun parse_mode="HTML" qo'shish tavsiya etiladi
    await message.answer(
        "<b>Assalomu alaykum!</b>\n\nKerakli bo'limni tanlang 👇", 
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "menu_regions")
async def show_regions(callback: CallbackQuery):
    # callback.answer() ni tekshirish shart emas, lekin yaxshi amaliyot
    await callback.answer("Viloyatlar ro'yxati yuklanmoqda...")
    
    await callback.message.edit_text(
        "<b>Viloyatni tanlang:</b>", 
        reply_markup=get_regions_keyboard(),
        parse_mode="HTML"
    )
