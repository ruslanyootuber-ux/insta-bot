import sys
import os

# MUHIM: Bu qator Python'ga botning asosiy papkasini (app/) ko'rsatadi.
# Natijada duo_data.py har qanday joydan (handlers ichidan ham) topiladi.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import asyncio
import logging
from aiohttp import web  # <-- Veb server uchun yangi import
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, dp

# Importlar
from handlers import start, menu_handlers, extra_handlers, admin_handlers
from handlers.extra_handlers import check_and_send_reminders
from handlers.zikr_handlers import router as zikr_router
from handlers.ramadan_handlers import router as ramadan_router
from handlers.qibla_handlers import router as qibla_router
from handlers.hadis_handlers import router as hadis_router
from handlers.tasbeh_handlers import router as tasbeh_router
from handlers.asmaul_handlers import router as asmaul_router
from handlers.duo_handlers import router as duo_router

# --- 1. API uchun maxsus funksiya (Mobil ilova uchun) ---
async def api_namoz_vaqtlari(request):
    # Hozircha namunaviy ma'lumot jo'natamiz. Keyin buni bazaga ulaymiz.
    data = {
        "mintaqa": "Yakkabog'",
        "sana": "28 Iyun, Yakshanba",
        "vaqtlar": {
            "bomdod": "03:32",
            "quyosh": "05:10",
            "peshin": "13:00",
            "asr": "17:45",
            "shom": "20:05",
            "xufton": "21:40"
        }
    }
    
    # CORS (Muhim!) - HTML ilovadan so'rov kelishiga ruxsat berish
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
    }
    return web.json_response(data, headers=headers)

# --- 2. Veb-serverni sozlash (Ilova ulanishi uchun) ---
async def start_web_server():
    app = web.Application()
    app.router.add_get('/api/namoz', api_namoz_vaqtlari)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logging.info("API server 8080-portda ishga tushdi...")

# --- 3. Botning ishlash jarayoni ---
async def on_startup():
    logging.info("Bot muvaffaqiyatli ishga tushdi!")

async def main():
    logging.basicConfig(level=logging.INFO)

    # Scheduler'ni sozlash
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=1)
    scheduler.start()

    # Routerlar
    dp.include_routers(
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
        duo_router    
    )

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    
    # ---> VEB SERVERNI ISHGA TUSHIRISH (Pollingdan oldin) <---
    await start_web_server()
    
    # ---> BOTNI ISHGA TUSHIRISH <---
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Dastur to'xtatildi.")
