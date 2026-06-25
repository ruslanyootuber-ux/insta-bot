from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# Bot obyekti (HTML formatida xabar yozish uchun parse_mode o'rnatilgan)
bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode="HTML")
)

# Barcha xabarlarni ushlab oluvchi Dispatcher
dp = Dispatcher()
