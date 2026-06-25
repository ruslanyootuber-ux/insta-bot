import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import handlers

# .env fayldan o'zgaruvchilarni yuklaydi
load_dotenv()

async def main():
    # Tokenni muhit o'zgaruvchisidan olish
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        raise ValueError("BOT_TOKEN topilmadi! .env faylni tekshiring.")

    bot = Bot(token=token)
    dp = Dispatcher()
    
    # Handlerlarni ulash
    dp.include_router(handlers.router)
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
