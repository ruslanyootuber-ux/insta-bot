# handlers/admin.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Loader orqali db ni import qilamiz
from loader import db, bot 

router = Router()

ADMIN_ID = 8727877170 

class Mailing(StatesGroup):
    text = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        users = db.get_all_users()
        await message.answer(
            f"👑 <b>Admin Panel</b>\n\n"
            f"👥 Jami foydalanuvchilar: <b>{len(users)}</b> ta\n\n"
            f"Habar yuborish uchun <b>/send</b> buyrug'ini yozing."
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
    text = message.text
    users = db.get_all_users() # Baza orqali barcha userlarni olamiz
    
    count = 0
    for user in users:
        user_id = user[0] # Bazadagi birinchi ustun (user_id)
        try:
            await bot.send_message(chat_id=user_id, text=text)
            count += 1
        except Exception:
            continue
            
    await message.answer(f"✅ Xabar <b>{count}</b> ta foydalanuvchiga yuborildi.")
    await state.clear()
