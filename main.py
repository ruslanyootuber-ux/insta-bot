import os
import time
import random
from instagrapi import Client

# Environment'dan olingan ma'lumotlar
USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")
TARGET_USERNAME = "qalampir.uz"

cl = Client()

# Sessiyani saqlash uchun fayl yo'li
session_file = "session.json"

def login():
    if os.path.exists(session_file):
        cl.load_settings(session_file)
        try:
            cl.login(USERNAME, PASSWORD)
        except Exception:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(session_file)
    else:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(session_file)

def run_bot():
    login()
    user_id = cl.user_id_from_username(TARGET_USERNAME)
    # Oxirgi post ID sini olish
    last_post = cl.user_medias(user_id, amount=1)[0]
    last_post_id = last_post.id
    
    print(f"Kuzatuv boshlandi: {TARGET_USERNAME}. Oxirgi post ID: {last_post_id}")
    
    comments = ["Ajoyib yangilik! 👍", "Doimiy kuzatib boramiz!", "Qiziqarli ma'lumot, rahmat! 😊"]

    while True:
        try:
            current_posts = cl.user_medias(user_id, amount=1)
            if not current_posts:
                time.sleep(600)
                continue
                
            new_post = current_posts[0]
            
            if new_post.id != last_post_id:
                print("Yangi post topildi! Izoh yozilmoqda...")
                cl.media_comment(new_post.id, random.choice(comments))
                last_post_id = new_post.id
            
            time.sleep(300) # Har 5 daqiqada tekshiradi
            
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(600) # Xato bo'lsa 10 daqiqa kutadi

if __name__ == "__main__":
    run_bot()