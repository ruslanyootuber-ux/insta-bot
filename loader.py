# loader.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage  # 1. Yangi import
from config import BOT_TOKEN
from database.db import Database 

# Tarmoq ulanishi vaqtini (timeout) 60 soniyagacha uzaytiramiz
session = AiohttpStorage = AiohttpSession(timeout=60)

# Bot instansiyasi
bot = Bot(
    token=BOT_TOKEN, 
    session=session, 
    default=DefaultBotProperties(parse_mode="HTML")
)

# 2. MemoryStorage ni Dispatcher ga ulaymiz
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Ma'lumotlar bazasini ishga tushiramiz
db = Database("data/main.db")
