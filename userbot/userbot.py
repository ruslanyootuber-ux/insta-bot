import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

# Global o'zgaruvchilar o'rniga faqat funksiya ichida chaqiramiz
async def advertiser():
    # O'zgaruvchilarni shu yerda o'qiymiz
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    session_str = os.getenv("SESSION_STRING")

    if not all([api_id, api_hash, session_str]):
        print("Xatolik: Secrets topilmadi! 5 soniyadan keyin qayta uriniladi...")
        await asyncio.sleep(5)
        return await advertiser() # Qayta urinish

    client = TelegramClient(StringSession(session_str), int(api_id), api_hash)
    await client.start()
    
    # ... reklamalar ro'yxati va sikl ...
    while True:
        # Reklama yuborish kodi
        await asyncio.sleep(300)
