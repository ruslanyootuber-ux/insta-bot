import sys
import os

# Papkani Python yo'liga qo'shish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# .env ni yuklash (serverda secret'lar bo'lsa ham, bu mahalliy test uchun kerak)
load_dotenv()

# Loader va boshqa importlar
from loader import bot, dp
from insta_worker.monitor import monitor_channel

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

async def on_startup():
    logging.info("Bot muvaffaqiyatli ishga tushirildi!")

async def run_namoz_bot():
    """Namoz bot qismi"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

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
    # Xavfsiz yuklash: agar None bo'lsa, xato bermaydi
    raw_api_id = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    CHANNEL_USERNAME = "@postbazauz"

    if raw_api_id is None or API_HASH is None:
        logging.error("XATOLIK: API_ID yoki API_HASH topilmadi! Fly secrets ni tekshiring.")
        return # Dasturni to'xtatish

    API_ID = int(raw_api_id)

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
