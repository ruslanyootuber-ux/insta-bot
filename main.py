import asyncio
import logging
from loader import bot, dp
# Endi start, menu_handlers va biz yaratgan extra_handlers ni import qilamiz
from handlers import start, menu_handlers, extra_handlers

async from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    scheduler = AsyncIOScheduler()
    # Har kuni soat 05:00 da ishga tushirish (misol uchun)
    scheduler.add_job(send_daily_reminders, 'cron', hour=5, minute=0)
    scheduler.start()
    # ... qolgan kodlar
 on_startup():
    print("Bot muvaffaqiyatli ishga tushdi va namoz vaqtlarini olishga tayyor!")

async def main():
    # Loglarni ekranga chiqarish
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Barcha routerlarni shu yerda ro'yxatdan o'tkazamiz
    # Bu qism botning "boshqaruv markazi" hisoblanadi
    dp.include_routers(
        start.router,
        menu_handlers.router,
        extra_handlers.router
    )

    # Bot ishga tushganda bajariladigan funksiya
    dp.startup.register(on_startup)

    # Pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
