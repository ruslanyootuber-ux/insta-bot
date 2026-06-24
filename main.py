import asyncio
import logging
import random
import os
from instagrapi import Client

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Konfiguratsiyalar (Fly.io secrets orqali olinadi)
SESSION_ID = os.getenv("SESSION_ID")

COMMENTS = [
    "🚀 Zo'r yangilik!", "🔥 Har doimgidek dolzarb mavzu.", "💡 Qiziqarli ma'lumotlar uchun rahmat.",
    "🙌 Buni kutgan edik!", "⚡️ Qalampir.uz - eng tezkor yangiliklar!", "✅ Foydali post bo'libdi.",
    "🧐 Juda qiziqarli, davomini kuting.", "🔝 O'zbekistondagi eng yaxshi yangiliklar kanali.",
    "📚 Rahmat, juda ma'lumotli post.", "🌟 Shunday yangiliklar ko'payib ketsin."
]

async def instagram_worker():
    cl = Client()
    # Sessiya orqali kirish (eng ishonchli usul)
    cl.login_by_sessionid(SESSION_ID)
    
    friend_id = cl.user_id_from_username("uzb_9577")
    target_id = cl.user_id_from_username("qalampir.uz")
    
    last_media_id = None
    last_processed_msg_id = None
    
    logger.info("Instagram worker ishga tushdi...")
    
    while True:
        try:
            # 1. Instagram post tekshirish
            medias = cl.user_medias(target_id, amount=1)
            if medias and medias[0].id != last_media_id:
                latest_media = medias[0]
                cl.media_comment(latest_media.id, random.choice(COMMENTS))
                cl.direct_send(f"Qalampir.uz dan yangi post: https://www.instagram.com/p/{latest_media.code}/", [friend_id])
                last_media_id = latest_media.id
                logger.info("Yangi post topildi va sharh yozildi.")
            
            # 2. Reels/Direct xabarlar reaksiya
            threads = cl.direct_threads(amount=3)
            for thread in threads:
                if thread.users[0].pk == friend_id:
                    msg = thread.messages[0]
                    if msg.item_type == "media" and msg.id != last_processed_msg_id:
                        cl.direct_message_reaction(msg.id, random.choice(["🔥", "❤️", "🫡", "🗿"]))
                        last_processed_msg_id = msg.id
                        
        except Exception as e:
            logger.error(f"Instagram xatosi: {e}")
        
        await asyncio.sleep(300) # 5 daqiqalik kutish

if __name__ == "__main__":
    asyncio.run(instagram_worker())
