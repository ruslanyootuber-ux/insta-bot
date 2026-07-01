import asyncio
import random
import os
from telethon import TelegramClient, events
from .insta_logic import upload_to_insta, insta_login

async def monitor_channel(api_id, api_hash, channel_username):
    client = TelegramClient('insta_session', api_id, api_hash)
    await client.start()
    insta_login()
    
    print("Kanal kuzatilmoqda...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        if event.message.photo:
            # 1. Rasmni yuklab olish
            path = await event.download_media()
            caption = event.message.message or "Yangi post"
            
            # 2. Random vaqt kutish (1 dan 2 soatgacha = 3600-7200 sekund)
            wait_time = random.randint(3600, 7200)
            print(f"Rasm olindi. {wait_time//60} daqiqadan keyin yuklanadi...")
            await asyncio.sleep(wait_time)
            
            # 3. Instagramga yuklash
            try:
                upload_to_insta(path, caption)
            finally:
                if os.path.exists(path):
                    os.remove(path) # Xotirani tozalash

    await client.run_until_disconnected()
