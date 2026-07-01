import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from .insta_logic import upload_to_insta, insta_login

async def monitor_channel(api_id, api_hash, channel_username, session_str):
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    await client.start()
    
    # Instagramga login qilish
    insta_login()
    
    print("Kanal kuzatilmoqda...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        if event.message.photo:
            path = await event.download_media()
            caption = event.message.message or "Yangi post"
            # Post yuklash
            await asyncio.to_thread(upload_to_insta, path, caption)
            if os.path.exists(path):
                os.remove(path)

    await client.run_until_disconnected()
