import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, dp
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import check_and_send_reminders
from handlers.zikr_handlers import router as zikr_router
 # Importni qo'shdik

async def on_startup():
    print("Bot muvaffaqiyatli ishga tushdi!")

async def main():
    logging.basicConfig(level=logging.INFO)

    # Scheduler'ni bir marta sozlaymiz
    scheduler = AsyncIOScheduler()
    
    # Har 1 daqiqada tekshirib turadigan eslatma tizimi
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    
    scheduler.start()

    # Routerlar
    dp.include_routers(
        start.router,
        menu_handlers.router,
        extra_handlers.router,
        dp.include_router(zikr_router)
    )

    dp.startup.register(on_startup)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")