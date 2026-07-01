import os
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from .insta_logic import upload_to_insta, insta_login

async def monitor_channel(api_id, api_hash, channel_username):
    # Secret nomini tekshiring: Fly.io da qanday kiritgan bo'lsangiz shunday bo'lishi kerak
    session_str = os.getenv("SESSION_STRING")
    
    # AGAR session_str bo'sh bo'lsa, kod ishlashni to'xtatishi kerak
    if not session_str:
        print("XATOLIK: SESSION_STRING topilmadi!")
        return

    # StringSession obyektini to'g'ri yaratish
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    
    # start() ichida bot tokeni bo'lmasa, u login so'raydi. 
    # Agar bu UserBot bo'lsa, string session bo'lishi shart.
    await client.start()
    insta_login()
    
    print("Kanal kuzatilmoqda...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        if event.message.photo:
            path = await event.download_media()
            caption = event.message.message or "Yangi post"
            wait_time = random.randint(3600, 7200)
            print(f"Rasm olindi. {wait_time//60} daqiqadan keyin yuklanadi...")
            await asyncio.sleep(wait_time)
            try:
                upload_to_insta(path, caption)
            finally:
                if os.path.exists(path):
                    os.remove(path)

    await client.run_until_disconnected()
