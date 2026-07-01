import os
from instagrapi import Client

client = Client()

# Instagram bot ekanligini sezmasligi uchun qurilma sozlamalari
# Bu sozlamalar Instagramga "Android telefonidan kiryapti" degan taassurot qoldiradi
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
        username = os.getenv("INSTA_USERNAME")
        password = os.getenv("INSTA_PASSWORD")
        
        if not username or not password:
            print("XATOLIK: INSTA_USERNAME yoki INSTA_PASSWORD secretlarda topilmadi!")
            return False
        
        print(f"Instagramga {username} orqali kirishga urinilmoqda...")
        client.login(username, password)
        print("Instagram login muvaffaqiyatli!")
        return True
    except Exception as e:
        print(f"DIQQAT: Instagramga kirishda xatolik: {e}")
        return False

def upload_to_insta(path, caption):
    try:
        # Agar mijoz hali login qilmagan bo'lsa, login qilamiz
        if not client.user_id:
            if not insta_login():
                return
            
        client.photo_upload(path, caption)
        print("Post Instagramga muvaffaqiyatli yuklandi!")
    except Exception as e:
        print(f"Instagram yuklashda xatolik: {e}")
        # Agar xatolik bo'lsa, sessiyani tozalab, keyingi safar qayta urinish uchun
        client.user_id = None
