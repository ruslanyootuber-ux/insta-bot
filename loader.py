from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# BOT_TOKEN config faylidan keladi
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Eski Database klassi va importi olib tashlandi.
# Endi funksiyalarni to'g'ridan-to'g'ri data.statistika_data dan chaqiramiz.
