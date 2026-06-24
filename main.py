import asyncio
import logging
import random
import os
from instagrapi import Client
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Konfiguratsiyalar
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
SESSION_ID = os.getenv("SESSION_ID")

COMMENTS = ["🚀 Zo'r yangilik!", "🔥 Har doimgidek dolzarb mavzu.", "✅ Foydali post bo'libdi.", "🎯 Juda o'rinli post.", "🚀 Zo'r, davom eting!"]
MESSAGES = ["Salom! Yangiliklarni kuzatib boring 🚀", "Foydali guruh ekan, rahmat! ✨", "Eng tezkor xabarlar shu yerda! 🔔"]

async def update_telegram_profile(client):
    """Profilni bir marta yangilash"""
    try:
        await client(functions.account.UpdateProfileRequest(
            first_name="Rasmiy",
            last_name="Yangiliklar",
            about="O'zbekistondagi eng tezkor yangiliklar kanali. Hamkorlik uchun: @admin"
        ))
        # Rasm qo'shish uchun: await client.upload_file('rasm.jpg') -> photos.UploadProfilePhotoRequest
        logger.info("Telegram profil yangilandi.")
    except Exception as e:
        logger.error(f"Profil yangilashda xato: {e}")

async def instagram_worker():
    cl = Client()
    cl.login_by_sessionid(SESSION_ID)
    friend_id = cl.user_id_from_username("uzb_9577")
    target_id = cl.user_id_from_username("qalampir.uz")
    last_media_id = None
    last_processed_msg_id = None
    
    while True:
        try:
            medias = cl.user_medias(target_id, amount=1)
            if medias and medias[0].id != last_media_id:
                latest_media = medias[0]
                cl.media_comment(latest_media.id, random.choice(COMMENTS))
                cl.direct_send(f"Qalampir.uz dan post: https://www.instagram.com/p/{latest_media.code}/", [friend_id])
                last_media_id = latest_media.id
            
            threads = cl.direct_threads(amount=3)
            for thread in threads:
                if thread.users[0].pk == friend_id:
                    msg = thread.messages[0]
                    if msg.item_type == "media" and msg.id != last_processed_msg_id:
                        cl.direct_message_reaction(msg.id, random.choice(["🔥", "❤️", "🫡", "🗿"]))
                        last_processed_msg_id = msg.id
        except Exception as e:
            logger.error(f"Instagram xatosi: {e}")
        await asyncio.sleep(300)

async def telegram_worker():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    
    # 1. Profilni yangilash
    await update_telegram_profile(client)
    
    while True:
        try:
            # Guruh qidirish
            result = await client(functions.contacts.SearchRequest(q="O'zbekiston", limit=5))
            for chat in result.chats:
                if isinstance(chat, types.Channel) or isinstance(chat, types.Chat):
                    try:
                        # Faqat yozish imkoniyati borligini tekshirish uchun xabar yuboramiz
                        await client.send_message(chat, random.choice(MESSAGES))
                        logger.info(f"Yuborildi: {chat.title}")
                    except: 
                        # Agar yuborib bo'lmasa, demak yozish taqiqlangan
                        continue
            
            # Mavjud guruhlarga yozish
            async for dialog in client.iter_dialogs(limit=10):
                if dialog.is_group or dialog.is_channel:
                    try:
                        await client.send_message(dialog, random.choice(MESSAGES))
                    except: continue
        except Exception as e:
            logger.error(f"Telegram xatosi: {e}")
        await asyncio.sleep(600)

async def main():
    await asyncio.gather(instagram_worker(), telegram_worker())

if __name__ == "__main__":
    asyncio.run(main())
