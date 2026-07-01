import os
import time
from instagrapi import Client

client = Client()

def insta_login():
    session_id = os.getenv("INSTA_SESSIONID")
    client.login_by_sessionid(session_id)
    print("Instagram login muvaffaqiyatli!")

def upload_to_insta(path, caption):
    # Rasm yuklash
    client.photo_upload(path, caption)
    print("Post Instagramga yuklandi!")
