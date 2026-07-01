import os
from instagrapi import Client

# Client'ni global darajada saqlaymiz
client = Client()

def insta_login():
    """Instagramga sessiya ID orqali kirish"""
    session_id = os.getenv("INSTA_SESSIONID")
    if not session_id:
        raise ValueError("INSTA_SESSIONID topilmadi! Iltimos, secrets ni tekshiring.")
    
    try:
        client.login_by_sessionid(session_id)
        print("Instagram login muvaffaqiyatli!")
    except Exception as e:
        print(f"Login qilishda xatolik: {e}")
        raise

def upload_to_insta(path, caption):
    """Rasmni Instagramga yuklash"""
    try:
        # Sessiya o'lgan bo'lsa, qayta login qilishni sinash
        if not client.get_settings():
            print("Sessiya eskirgan, qayta login qilinmoqda...")
            insta_login()
            
        client.photo_upload(path, caption)
        print("Post Instagramga yuklandi!")
    except Exception as e:
        print(f"Instagram yuklashda xatolik: {e}")
        # Yuklashda xatolik bo'lsa, logga yozamiz
