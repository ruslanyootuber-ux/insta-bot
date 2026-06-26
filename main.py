import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, dp
# admin_handlers ni import qilgan ekansiz, uni ham qo'shamiz
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import check_and_send_reminders
from handlers.zikr_handlers import router as zikr_router
from handlers.ramadan_handlers import router as ramadan_router
from handlers.qibla_handlers import router as qibla_router
from handlers.hadis_handlers import router as hadis_router
from handlers.tasbeh_handlers import router as tasbeh_router
from handlers.asmaul_handlers import router as asmaul_router

async def on_startup():
    print("Bot muvaffaqiyatli ishga tushdi!")

async def main():
    logging.basicConfig(level=logging.INFO)

    # Scheduler'ni sozlash
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

    # Routerlar
    # Eslatma: admin_handlers.router ni qo'shishni unutmang!
    dp.include_routers(
        start.router,
        menu_handlers.router,
        extra_handlers.router,
        admin_handlers.router,  
        zikr_router,
        qibla_router,
        ramadan_router,
        hadis_router, 
        tasbeh_router' 
        asmaul_router         
    )

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")