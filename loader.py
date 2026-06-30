# loader.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession  # Yangi import
from config import BOT_TOKEN
from database.db import Database  # Ma'lumotlar bazasi klassini import qilamiz

# Tarmoq ulanishi vaqtini (timeout) 60 soniyagacha uzaytiramiz
session = AiohttpSession(timeout=60)

# Bot instansiyasi (HTML rejimida va xavfsiz sessiya bilan)
bot = Bot(
    token=BOT_TOKEN, 
    session=session, 
    default=DefaultBotProperties(parse_mode="HTML")
)

# Dispatcher instansiyasi
dp = Dispatcher()

# Ma'lumotlar bazasini ishga tushiramiz va 'db' o'zgaruvchisini yaratamiz
db = Database("data/main.db")  # Agar baza fayli boshqa yerda bo'lsa, manzilni o'zgartirishingiz mumkin
