import time
import logging
import random
from instagrapi import Client
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 30 ta namuna matn
COMMENTS = [
    "Zo'r yangilik!", "Har doimgidek dolzarb mavzu.", "Qiziqarli ma'lumotlar uchun rahmat.",
    "Buni kutgan edik!", "Qalampir.uz - eng tezkor yangiliklar!", "Foydali post bo'libdi.",
    "Juda qiziqarli, davomini kuting.", "O'zbekistondagi eng yaxshi yangiliklar kanali.",
    "Rahmat, juda ma'lumotli post.", "Shunday yangiliklar ko'payib ketsin.",
    "Ajoyib ma'lumot!", "Buni barchaga ulashish kerak.", "Qalampir.uz jamoasiga omad!",
    "Ishingizga rivoj!", "Yaxshi tahlil qilibsiz.", "Juda o'rinli post.",
    "Yangiliklar uchun rahmat.", "Menga juda yoqdi.", "Kutgan edik shuni.",
    "Juda ham foydali.", "Doimo birinchi o'rinda!", "Ishonchli xabar.",
    "Jamoangizga rahbarlik ishlaringizda omad.", "Sifatli kontent.", "Zo'r, davom eting!",
    "Buni bilmagan ekanman, rahmat.", "Qoyil, tezkorlik uchun rahmat.",
    "Eng so'nggi xabarlar faqat sizda.", "Ajoyib ish bo'libdi.", "Katta rahmat!", "Nexia2 Legenda?"
]

def run_bot():
    session_id = os.getenv("SESSION_ID")
    cl = Client()
    
    try:
        logger.info("Sessiya orqali kirilmoqda...")
        cl.login_by_sessionid(session_id)
        
        # Qalampir.uz ning user_id sini olish
        target_username = "qalampir.uz"
        user_id = cl.user_id_from_username(target_username)
        last_media_id = None
        
        logger.info(f"Bot ishga tushdi! {target_username} kuzatilmoqda...")
        
        while True:
            # Eng oxirgi postni olish
            medias = cl.user_medias(user_id, amount=1)
            if medias:
                latest_media = medias[0]
                
                # Agar bu yangi post bo'lsa
                if latest_media.id != last_media_id:
                    comment_text = random.choice(COMMENTS)
                    cl.media_comment(latest_media.id, comment_text)
                    logger.info(f"Yangi post topildi! Izoh yozildi: '{comment_text}'")
                    last_media_id = latest_media.id
                else:
                    logger.info("Yangi post topilmadi, kutib turibman...")
            
            # Instagram bloklamasligi uchun har 10-15 daqiqada tekshirish tavsiya etiladi
            time.sleep(600) 
            
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    run_bot()
