from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

# MemoryStorage - FSM (holatlar) uchun vaqtinchalik xotira
storage = MemoryStorage()

# Bot instansiyasi
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

# Dispatcherga storage ni ulaymiz
dp = Dispatcher(storage=storage)
