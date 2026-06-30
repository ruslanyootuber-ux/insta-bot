import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database.db import Database 

# 1. Tarmoq ulanishi vaqtini (timeout) 60 soniyagacha uzaytiramiz
session = AiohttpSession(timeout=60)

# 2. Bot instansiyasi
bot = Bot(
    token=BOT_TOKEN, 
    session=session, 
    default=DefaultBotProperties(parse_mode="HTML")
)

# 3. MemoryStorage ni Dispatcher ga ulaymiz
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# 4. Ma'lumotlar bazasini ishga tushiramiz (data papkasi yo'q bo'lsa yaratamiz)
if not os.path.exists("data"):
    os.makedirs("data")

db = Database("data/main.db")
