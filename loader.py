from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# Bot instansiyasi
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# Dispatcher (storage'siz sodda holatda)
dp = Dispatcher()
