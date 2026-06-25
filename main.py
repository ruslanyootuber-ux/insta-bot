import asyncio
import logging
from loader import bot, dp

# Kelajakda handlerlarni bu yerga ulaymiz
# from handlers import start_handler 

async def on_startup():
    print("Bot muvaffaqiyatli ishga tushdi va namoz vaqtlarini olishga tayyor!")

async def main():
    # Loglarni ekranga chiqarish (xatoliklarni ko'rib turish uchun)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    
    # Kelajakda routerlarni bu yerda ro'yxatdan o'tkazamiz
    # dp.include_router(start_handler.router)
    
    # Bot ishga tushganda bajariladigan funksiya
    dp.startup.register(on_startup)
    
    # Pollingni boshlash (bot doimiy ishlab turishi uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
