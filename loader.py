# loader.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from database.db import Database  # Ma'lumotlar bazasi klassini import qilamiz

# Bot instansiyasi (HTML rejimida)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# Dispatcher instansiyasi
dp = Dispatcher()

# Ma'lumotlar bazasini ishga tushiramiz va 'db' o'zgaruvchisini yaratamiz
db = Database("data/main.db")  # Agar baza fayli boshqa yerda bo'lsa, manzilni o'zgartirishingiz mumkin
