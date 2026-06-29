from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

# Importlar
from data.statistika_data import count_users, get_all_users_ids, delete_user

router = Router()

ADMIN_ID = 8727877170 

class Mailing(StatesGroup):
    text = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        users_count = count_users()
        await message.answer(
            f"👑 <b>Admin Panel</b>\n\n"
            f"👥 Jami foydalanuvchilar: {users_count} ta\n\n"
            f"Barcha foydalanuvchilarga xabar yuborish uchun /send buyrug'ini bosing."
        )
    else:
        await message.answer("❌ Siz admin emassiz!")

@router.message(Command("send"))
async def mailing_start(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.answer("📩 Foydalanuvchilarga yuboriladigan xabarni yozing:")
        await state.set_state(Mailing.text)
    else:
        await message.answer("❌ Siz admin emassiz!")

@router.message(Mailing.text)
async def mailing_process(message: Message, state: FSMContext):
    users = get_all_users_ids() 
    count = 0
    
    msg = await message.answer("⏳ Xabar yuborilmoqda, kuting...")
    
    for user_id in users:
        try:
            # message.bot orqali bot instansiyasini chaqiramiz
            await message.bot.send_message(user_id, message.text)
            count += 1
            # Telegram limitlariga tushmaslik uchun kichik pauza
            await asyncio.sleep(0.05) 
        except Exception:
            # Agar foydalanuvchi botni bloklagan bo'lsa, bazadan o'chirib tashlaymiz
            delete_user(user_id)
            
    await msg.edit_text(f"✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!")
    await state.clear()
