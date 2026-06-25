from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from loader import db, bot

router = Router()

# Admin ID sini kiriting (Telegramda @userinfobot orqali o'z IDingizni bilib oling)
ADMIN_ID = 123456789  # O'z IDingizni yozing

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        users_count = len(db.get_all_users())
        await message.answer(
            f"👑 <b>Admin Panel</b>\n\n"
            f"👥 Jami foydalanuvchilar: {users_count} ta\n\n"
            f"Botni boshqarish uchun pastdagi tugmalardan foydalaning (kelajakda qo'shiladi)."
        )
    else:
        await message.answer("❌ Siz admin emassiz!")
