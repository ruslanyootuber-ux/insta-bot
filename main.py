import os
import logging
from instagrapi import Client

# Loglarni ko'rish uchun sozlama
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def run_bot():
    # 1. Fly.io secret'dan SESSION_ID ni o'qib olish
    session_id = os.getenv("SESSION_ID")
    
    if not session_id:
        logger.error("SESSION_ID topilmadi! Iltimos, fly secrets orqali o'rnating.")
        return

    cl = Client()
    
    try:
        # 2. Sessiya orqali kirish
        logger.info("Instagram'ga sessiya orqali kirilmoqda...")
        cl.login_by_sessionid(session_id)
        logger.info("Muvaffaqiyatli kirildi!")
        
        # 3. Botingizning asosiy vazifalari shu yerda bajariladi
        # Misol: Profil ma'lumotlarini olish
        user_info = cl.account_info()
        logger.info(f"Salom, {user_info.username}! Bot ishga tushdi.")
        
        # SHU YERDA O'Z KODINGIZNI YOZING
        # Masalan: cl.media_upload("photo.jpg", "caption")
        
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    run_bot()
