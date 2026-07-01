import os
from instagrapi import Client

client = Client()

def insta_login():
    session_id = os.getenv("INSTA_SESSIONID")
    client.login_by_sessionid(session_id)
    print("Instagram login muvaffaqiyatli!")

def upload_to_insta(path, caption):
    try:
        if not client.get_settings():
            insta_login()
        client.photo_upload(path, caption)
        print("Post Instagramga yuklandi!")
    except Exception as e:
        print(f"Instagram yuklashda xatolik: {e}")
