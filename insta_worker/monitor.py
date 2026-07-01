import asyncio
import random
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from .insta_logic import upload_to_insta, insta_login

async def monitor_channel(api_id, api_hash, channel_username, session_str):
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    await client.start()
    insta_login()
    
    print("Kanal kuzatilmoqda...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        if event.message.photo:
            path = await event.download_media()
            caption = event.message.message or "Yangi post"
            wait_time = random.randint(3600, 7200)
            await asyncio.sleep(wait_time)
            try:
                upload_to_insta(path, caption)
            finally:
                if os.path.exists(path):
                    os.remove(path)

    await client.run_until_disconnected()
