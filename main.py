import asyncio
import logging
import random
import os
import requests
from instagrapi import Client

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

SESSION_ID = os.getenv("SESSION_ID")

COMMENTS = [
    "🚀 Zo'r yangilik!", "🔥 Har doimgidek dolzarb mavzu.", "💡 Qiziqarli ma'lumotlar uchun rahmat.",
    "🙌 Buni kutgan edik!", "⚡️ Qalampir.uz - eng tezkor yangiliklar!", "✅ Foydali post bo'libdi."
]

TAGS = [
    "#uzbekistan #tashkent #yangiliklar #uzb #reels #trend #top #qiziqarli #foydali #hayot #uz",
    "#faktlar #olimlar #ilm #texnologiya #dunyoyuzida #obuna #like #comment #aktiv #reelsinstagram",
    "#motivation #muvaffaqiyat #biznes #ibrat #hayotiy #fikr #uzbek #samarkand #bukhara #fergana",
    "#reels #instagramreels #reelsinstagram #reelsvideo #viral #trending #explore #foryou #foryoupage #fyp #reelsviral #instadaily #trendingnow #reelsindia #reelschallenge #instalike",
    "#uzbekistan #tashkent #uzb #toshkent #uzbek #uzbekreels #reelsuz #uzbekistan_inst #samarkand #bukhara #andijan #fergana #uzbektv #o‘zbekiston #uzbekcha",
    "#reels #trending #explore"
    # ... bu yerga yana 40+ tag qo'shishingiz mumkin
]

async def instagram_worker():
    cl = Client()
    cl.login_by_sessionid(SESSION_ID)
    
    friend_id = cl.user_id_from_username("uzb_9577")
    target_id = cl.user_id_from_username("qalampir.uz")
    
    last_media_id = None
    last_processed_msg_id = None
    
    # Rasm yuklash uchun vaqt hisoblagich
    last_post_time = 0 
    
    logger.info("Instagram worker va Poster ishga tushdi...")
    
    while True:
        try:
            # --- 1. POSTER QISMI (Har 15 daqiqada) ---
            current_time = asyncio.get_event_loop().time()
            if current_time - last_post_time > 900: # 900 sekund = 15 daqiqa
                # Tasodifiy rasm yuklab olish
                img_data = requests.get("https://picsum.photos/1080/1080").content
                with open("temp.jpg", "wb") as f: f.write(img_data)
                
                # Taglarni tanlash
                caption = f"Qiziqarli ma'lumot! {random.choice(TAGS)}"
                cl.photo_upload("temp.jpg", caption)
                
                last_post_time = current_time
                logger.info("Yangi post avtomatik joylandi.")

            # --- 2. KUZATUV QISMI (Mavjud kod) ---
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
                        cl.direct_message_reaction(msg.id, random.choice(["🔥", "🗿", "🫡", "❤️"]))
                        last_processed_msg_id = msg.id
                        
        except Exception as e:
            logger.error(f"Xatolik: {e}")
        
        await asyncio.sleep(60) # Har daqiqa tekshiradi

if __name__ == "__main__":
    asyncio.run(instagram_worker())
