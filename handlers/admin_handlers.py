from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loader import db, bot

router = Router()

# O'z IDingizni shu yerga yozing
ADMIN_ID = 8727877170 

# Xabar yuborish uchun holatlar (FSM)
class Mailing(StatesGroup):
    text = State()

@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        users_count = len(db.get_all_users())
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
    users = db.get_all_users()
    count = 0
    
    await message.answer("⏳ Xabar yuborilmoqda, kuting...")
    
    for user in users:
        try:
            # user[0] bu bazadagi user_id
            await bot.send_message(user[0], message.text)
            count += 1
        except Exception:
            # Agar foydalanuvchi botni bloklagan bo'lsa, xatolikni o'tkazib yuboramiz
            continue
            
    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!")
    await state.clear()