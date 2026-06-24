import time
import logging
import random
from instagrapi import Client
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

COMMENTS = [
    "🚀 Zo'r yangilik!", "🔥 Har doimgidek dolzarb mavzu.", "💡 Qiziqarli ma'lumotlar uchun rahmat.",
    "🙌 Buni kutgan edik!", "⚡️ Qalampir.uz - eng tezkor yangiliklar!", "✅ Foydali post bo'libdi.",
    "🧐 Juda qiziqarli, davomini kuting.", "🔝 O'zbekistondagi eng yaxshi yangiliklar kanali.",
    "📚 Rahmat, juda ma'lumotli post.", "🌟 Shunday yangiliklar ko'payib ketsin.",
    "💎 Ajoyib ma'lumot!", "📢 Buni barchaga ulashish kerak.", "🍀 Qalampir.uz jamoasiga omad!",
    "📈 Ishingizga rivoj!", "🔍 Yaxshi tahlil qilibsiz.", "🎯 Juda o'rinli post.",
    "📰 Yangiliklar uchun rahmat.", "❤️ Menga juda yoqdi.", "🕒 Kutgan edik shuni.",
    "🧠 Juda ham foydali.", "🥇 Doimo birinchi o'rinda!", "🛡 Ishonchli xabar.",
    "🤝 Jamoangizga rahbarlik ishlaringizda omad.", "🎬 Sifatli kontent.", "🚀 Zo'r, davom eting!",
    "✨ Buni bilmagan ekanman, rahmat.", "👏 Qoyil, tezkorlik uchun rahmat.",
    "🔔 Eng so'nggi xabarlar faqat sizda.", "🎨 Ajoyib ish bo'libdi.", "🙏 Katta rahmat!", 
    "🚗 Nexia2 Legenda? 😎"
]

def run_bot():
    session_id = os.getenv("SESSION_ID")
    friend_username = "uzb_9577"  # Do'stingizning logini
    cl = Client()
    
    try:
        cl.login_by_sessionid(session_id)
        user_id = cl.user_id_from_username("qalampir.uz")
        friend_id = cl.user_id_from_username(friend_username)
        
        last_media_id = None
        last_processed_msg_id = None
        
        logger.info("Bot ishga tushdi!")
        
        while True:
            # 1. Qalampir.uz ni tekshirish va komment yozish
            medias = cl.user_medias(user_id, amount=1)
            if medias and medias[0].id != last_media_id:
                latest_media = medias[0]
                cl.media_comment(latest_media.id, random.choice(COMMENTS))
                last_media_id = latest_media.id
                
                # Qalampir.uz dan yangi post chiqqanda do'stga yuborish
                cl.direct_send(f"Qalampir.uz dan yangi post: https://www.instagram.com/p/{latest_media.code}/", [friend_id])
                logger.info("Do'stga yangi post yuborildi.")

            # 2. Do'stning Reelslariga reaksiya bildirish
            threads = cl.direct_threads(amount=5)
            for thread in threads:
                if thread.users[0].pk == friend_id:
                    last_msg = thread.messages[0]
                    if last_msg.item_type == "media" and last_msg.id != last_processed_msg_id:
                        cl.direct_message_reaction(last_msg.id, random.choice(["🔥", "❤️", "🫡", "🗿", "😂", "👍"]))
                        last_processed_msg_id = last_msg.id
                        logger.info("Do'stning Reelsiga reaksiya bildirildi.")
            
            time.sleep(300) # 5 daqiqalik interval
            
    except Exception as e:
        logger.error(f"Xatolik: {e}")

if __name__ == "__main__":
    run_bot()
