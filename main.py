# main.py

import sys
import os
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from loader import bot, dp
from data import asmaul_husna_data, hadis_data, zikr_data, tasbeh_data, duo_data, suralar_data

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
from handlers.audio_id_handler import router as audio_id_router  # <-- Янги аудио ИД роутери

async def main():
    logging.basicConfig(level=logging.INFO)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

    # Ортиқча media_router олиб ташланди ва янги аудио роутер қўшилди
    dp.include_routers(
        audio_id_router,  # Текширув тез ишлаши учун энг тепага қўйдик
        start.router, 
        menu_handlers.router, 
        extra_handlers.router, 
        admin_handlers.router,
        zikr_router, 
        qibla_router, 
        ramadan_router, 
        hadis_router,
        tasbeh_router, 
        asmaul_router, 
        duo_router, 
        taxorat_router,
        erkaklar_namozi_router,
        ayollar_namozi_router,
        suralar_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Dastur to'xtatildi.")
