from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Baza funksiyalari
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
    
    await message.answer("⏳ Xabar yuborilmoqda, kuting...")
    
    for user_id in users:
        try:
            await message.bot.send_message(user_id, message.text)
            count += 1
        except Exception:
            delete_user(user_id)
            
    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!")
    await state.clear()
