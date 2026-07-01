import os
from instagrapi import Client

client = Client()

# Instagram bot ekanligini sezmasligi uchun qurilma sozlamalari
client.set_device({
    "app_version": "275.0.0.27.98",
    "android_version": 29,
    "android_sdk": 29,
    "manufacturer": "Google",
    "model": "Pixel 4",
    "pixel_density": "420dpi",
    "resolution": "1080x1920"
})

def insta_login():
    try:
        session_id = os.getenv("INSTA_SESSIONID")
        if not session_id:
            print("XATOLIK: INSTA_SESSIONID topilmadi!")
            return
        
        client.login_by_sessionid(session_id)
        print("Instagram login muvaffaqiyatli!")
    except Exception as e:
        print(f"DIQQAT: Instagramga kirishda xatolik: {e}")

def upload_to_insta(path, caption):
    try:
        # Sessiya faolligini tekshirish
        if not client.user_id:
            insta_login()
            
        client.photo_upload(path, caption)
        print("Post Instagramga yuklandi!")
    except Exception as e:
        print(f"Instagram yuklashda xatolik: {e}")
