import sys
import os
import asyncio
import logging
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Asosiy yo'lni qo'shish
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from loader import bot, dp
# Data papkasidagi fayllarni import qilish
from data import asmaul_husna_data, hadis_data, zikr_data, tasbeh_data, duo_data
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import check_and_send_reminders
from handlers.zikr_handlers import router as zikr_router
from handlers.ramadan_handlers import router as ramadan_router
from handlers.qibla_handlers import router as qibla_router
from handlers.hadis_handlers import router as hadis_router
from handlers.tasbeh_handlers import router as tasbeh_router
from handlers.asmaul_handlers import router as asmaul_router
from handlers.duo_handlers import router as duo_router

# --- API Handler ---
async def api_handler(request):
    func = request.match_info.get('func')
    
    if func == 'asmaul':
        return web.json_response(asmaul_husna_data.data, headers={"Access-Control-Allow-Origin": "*"})
    elif func == 'hadis':
        return web.json_response(hadis_data.data, headers={"Access-Control-Allow-Origin": "*"})
    elif func == 'zikr':
        return web.json_response(zikr_data.data, headers={"Access-Control-Allow-Origin": "*"})
    else:
        return web.json_response({"error": "Bunday bo'lim topilmadi"}, status=404)

async def start_web_server():
    app = web.Application()
    # Dinamik yo'l
    app.router.add_get('/api/{func}', api_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logging.info("API server 8080-portda ishga tushdi...")

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

    dp.include_routers(
        start.router, menu_handlers.router, extra_handlers.router, admin_handlers.router,
        zikr_router, qibla_router, ramadan_router, hadis_router,
        tasbeh_router, asmaul_router, duo_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error(f"Xatolik: {e}")
            import time
            time.sleep(5)
