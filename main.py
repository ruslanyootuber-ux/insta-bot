import os
import random
import time
from instagrapi import Client

cl = Client()

# Session stringni Fly.io'dan o'qiydi
session_id = os.getenv("SESSION_ID")
if not session_id:
    print("Xato: SESSION_ID topilmadi!")
    exit()

cl.login_by_sessionid(session_id)
cl.login_by_sessionid(session_id)

def start_bot():
    # Yangi Reels'lar qidirish uchun hashtaglar
    hashtags = ["uzbekistan", "tashkent", "uzb"]
    comments = ["Zo'r video!", "Qoyil!", "Ajoyib!", "Like bosdim!", "Yaxshi chiqibdi!"]
    
    while True:
        try:
            tag = random.choice(hashtags)
            medias = cl.hashtag_medias_recent(tag, amount=5)
            
            for media in medias:
                # Like bosish
                cl.media_like(media.id)
                # Komment yozish
                cl.media_comment(media.id, random.choice(comments))
                print(f"Reels ID: {media.id} ga like va komment bosildi.")
                # Har bir harakatdan keyin tasodifiy dam olish (Spamdan himoya)
                time.sleep(random.randint(300, 900))
                
        except Exception as e:
            import time
# ... sizning botingiz kodlari ...

print("Bot ishni tugatdi, lekin uxlab turibdi...")
while True:
    time.sleep(3600)  # Bot 1 soat davomida uxlab, serverni ushlab turadi
