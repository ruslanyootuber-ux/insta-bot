import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, dp
# Barcha handlerlarni bitta qatorda import qilamiz
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import send_daily_reminders 

async def on_startup():
    print("Bot muvaffaqiyatli ishga tushdi va namoz vaqtlarini olishga tayyor!")

async def main():
    # Loglarni sozlash
    logging.basicConfig(level=logging.INFO)

    # Scheduler sozlamasi
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_reminders, 'cron', hour=5, minute=0)
    scheduler.start()

    # Barcha routerlarni ro'yxatdan o'tkazamiz
    dp.include_routers(
        start.router,
        menu_handlers.router,
        extra_handlers.router,
        admin_handlers.router # Admin router ham qo'shildi
    )

    dp.startup.register(on_startup)

    # Pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")