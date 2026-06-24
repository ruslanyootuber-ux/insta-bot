import asyncio
import logging
import random
import os
import requests
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

COMMENTS = [
    "🚀 Zo'r yangilik!", "🔥 Har doimgidek dolzarb mavzu.", "💡 Qiziqarli ma'lumotlar uchun rahmat.",
    "🙌 Buni kutgan edik!", "⚡️ Qalampir.uz - eng tezkor yangiliklar!", "✅ Foydali post bo'libdi.",
    "🧐 Juda qiziqarli, davomini kuting.", "🔝 O'zbekistondagi eng yaxshi yangiliklar kanali."
]

MESSAGES = [
    "Salom! Yangiliklarni kuzatib boring 🚀", 
    "Foydali guruh ekan, rahmat! ✨",
    "Eng tezkor xabarlar shu yerda! 🔔"
]

# --- Instagram Worker ---
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
                        cl.direct_message_reaction(msg.id, random.choice(["🔥", "❤️", "🫡", "👍"]))
                        last_processed_msg_id = msg.id
        except Exception as e:
            logger.error(f"Instagram xatosi: {e}")
        await asyncio.sleep(300)

# --- Telegram Worker ---
async def telegram_worker():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    
    # Profilni yangilash
    try:
        await client(functions.account.UpdateProfileRequest(
            first_name="Test",
            about="O'zbekistondagi eng tezkor yangiliklar kanali."
        ))
        response = requests.get("https://picsum.photos/200")
        with open("avatar.jpg", "wb") as f: f.write(response.content)
        file = await client.upload_file("avatar.jpg")
        await client(functions.photos.UploadProfilePhotoRequest(file=file))
        logger.info("Profil muvaffaqiyatli yangilandi!")
    except Exception as e:
        logger.error(f"Profil yangilashda xato: {e}")

    while True:
        try:
            # Guruh qidirish
            result = await client(functions.contacts.SearchRequest(q="O'zbekiston", limit=5))
            for chat in result.chats:
                try:
                    await client(functions.channels.JoinChannelRequest(chat))
                    await client.send_message(chat, random.choice(MESSAGES))
                except: continue
            
            # Dialoglarni iteratsiya qilish (to'g'rilangan)
            async for dialog in client.iter_dialogs():
                if dialog.is_group or dialog.is_channel:
                    try:
                        await client.send_message(dialog, random.choice(MESSAGES))
                    except: continue
        except Exception as e:
            logger.error(f"Telegram umumiy xatosi: {e}")
        await asyncio.sleep(600)

async def main():
    await asyncio.gather(instagram_worker(), telegram_worker())

if __name__ == "__main__":
    asyncio.run(main())
