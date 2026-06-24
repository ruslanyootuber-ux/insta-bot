import asyncio
import logging
import random
import os
import requests
from instagrapi import Client
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Konfiguratsiyalar
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
SESSION_ID = os.getenv("SESSION_ID")
BOT_TOKEN = "8234989129:AAFyNtKEbNnAzm_Z7tBvC1iJ79WZXKWPtnI"      # O'zingizning haqiqiy tokenni shu yerga qo'ying

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Bot Interaktiv qismi ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Salom! Bot ishlamoqda. Instagram va Telegram avtomatlashtirish jarayonlari faol! 🚀")

# --- Instagram Worker ---
async def instagram_worker():
    cl = Client()
    cl.login_by_sessionid(SESSION_ID)
    friend_id = cl.user_id_from_username("uzb_9577")
    target_id = cl.user_id_from_username("qalampir.uz")
    last_media_id = None
    
    while True:
        try:
            medias = cl.user_medias(target_id, amount=1)
            if medias and medias[0].id != last_media_id:
                latest_media = medias[0]
                cl.media_comment(latest_media.id, random.choice(["🚀 Ajoyib!", "🔥 Zo'r!"]))
                last_media_id = latest_media.id
        except Exception as e:
            logger.error(f"Instagram xatosi: {e}")
        await asyncio.sleep(300)

# --- Telegram Worker ---
async def telegram_worker():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    
    while True:
        try:
            async for dialog in client.iter_dialogs():
                if dialog.is_group:
                    await client.send_message(dialog, "Salom! Yangiliklarni kuzatib boring 🚀")
        except Exception as e:
            logger.error(f"Telegram xatosi: {e}")
        await asyncio.sleep(600)

# --- Asosiy qism ---
async def main():
    # Bot polling va workerlarni bir vaqtda ishga tushirish
    await asyncio.gather(
        dp.start_polling(bot),
        instagram_worker(),
        telegram_worker()
    )

if __name__ == "__main__":
    asyncio.run(main())
