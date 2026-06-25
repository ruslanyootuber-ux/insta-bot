import asyncio
from aiogram import Bot, Dispatcher
import handlers

# Tokeningizni shu yerga yozing (yoki os.getenv dan foydalaning)
TOKEN = "YOUR_BOT_TOKEN_HERE"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Handlerlarni ulash
    dp.include_router(handlers.router)
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
