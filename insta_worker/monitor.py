import asyncio
import random
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from .insta_logic import upload_to_insta, insta_login

async def monitor_channel(api_id, api_hash, channel_username):
    # Serverdan SESSION_STRING ni o'qib olamiz
    session_str = os.getenv("SESSION_STRING")
    
    # StringSession yordamida ulanamiz (Fayl yaratilmaydi, bu resursni tejaydi)
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    
    await client.start()
    insta_login()
    
    print("Kanal kuzatilmoqda...")

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        # Faqat rasm (photo) bo'lsa ishlaydi
        if event.message.photo:
            # 1. Rasmni yuklab olish
            path = await event.download_media()
            caption = event.message.message or "Yangi post"
            
            # 2. Random vaqt kutish (3600-7200 sekund)
            wait_time = random.randint(3600, 7200)
            print(f"Rasm olindi. {wait_time//60} daqiqadan keyin yuklanadi...")
            
            # Kutish jarayonida bot ishlashda davom etadi
            await asyncio.sleep(wait_time)
            
            # 3. Instagramga yuklash
            try:
                upload_to_insta(path, caption)
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
            finally:
                if os.path.exists(path):
                    os.remove(path) # Xotirani tozalash

    # Bot uzilib qolmasligi uchun
    await client.run_until_disconnected()
