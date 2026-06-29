from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

ADMIN_ID = 8727877170 

class Mailing(StatesGroup):
    text = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            f"👑 <b>Admin Panel</b>\n\n"
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
    # Eslatma: Bazadan foydalanuvchilarni ololmaymiz, chunki baza funksiyalari o'chirilgan.
    # Agar xabar yuborish kerak bo'lsa, foydalanuvchilar ro'yxati (IDs) qayerdandir kelishi kerak.
    
    await message.answer("⚠️ Baza ulanmagani uchun xabar yuborish funksiyasi cheklangan.")
    await state.clear()
