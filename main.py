import asyncio
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Loader va boshqa importlar
from loader import bot, dp
from instagram_bot.monitor import monitor_channel

# Handler importlari
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import check_and_send_reminders
from handlers.zikr_handlers import router as zikr_router
from handlers.ramadan_handlers import router as ramadan_router
from handlers.qibla_handlers import router as qibla_router
from handlers.hadis_handlers import router as hadis_router
from handlers.tasbeh_handlers import router as tasbeh_router
from handlers.asmaul_handlers import router as asmaul_router
from handlers.duo_handlers import router as duo_router
from handlers.taxorat_handlers import router as taxorat_router
from handlers.erkaklar_namozi_handlers import router as erkaklar_namozi_router
from handlers.ayollar_namozi_handlers import router as ayollar_namozi_router
from handlers.suralar_handlers import router as suralar_router
from handlers.audio_id_handler import router as audio_id_router
from handlers.masjid_handlers import router as masjid_router

# .env ni yuklash (API_ID, HASH larni olish uchun)
load_dotenv()

async def on_startup():
    logging.info("Bot muvaffaqiyatli ishga tushirildi!")

async def run_namoz_bot():
    """Namoz bot qismi"""
    # Logging sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Scheduler ni sozlash
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

    # Routerlarni ulash
    dp.include_routers(
        start.router, admin_handlers.router, menu_handlers.router,
        audio_id_router, extra_handlers.router, masjid_router,
        zikr_router, qibla_router, ramadan_router, hadis_router,
        tasbeh_router, asmaul_router, duo_router, taxorat_router,
        erkaklar_namozi_router, ayollar_namozi_router, suralar_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)

async def main():
    # Instagram uchun sozlamalar (bularni .env dan olish yaxshi)
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    CHANNEL_USERNAME = "@postbazauz" # Kanalingiz ID yoki Username-i

    # Ikkala botni parallel ishga tushirish
    try:
        await asyncio.gather(
            run_namoz_bot(),
            monitor_channel(API_ID, API_HASH, CHANNEL_USERNAME)
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
