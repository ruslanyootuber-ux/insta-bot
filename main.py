import os
import asyncio
import requests
from instagrapi import Client

# Rasm yuklab olish uchun funksiya
def download_random_image(filename="post.jpg"):
    url = "https://picsum.photos/1080/1080" # Tasodifiy rasm
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

async def post_worker():
    session_id = os.getenv("SESSION_ID")
    cl = Client()
    cl.login_by_sessionid(session_id)
    
    while True:
        try:
            print("Rasm yuklab olinmoqda...")
            download_random_image()
            
            print("Instagramga post qilinmoqda...")
            cl.photo_upload("post.jpg", "Tasodifiy post #bot")
            print("Post muvaffaqiyatli yuklandi!")
            
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
        
        # 10 daqiqa kutish (600 soniya)
        await asyncio.sleep(10)

async def keep_alive():
    while True:
        await asyncio.sleep(60)

async def main():
    await asyncio.gather(post_worker(), keep_alive())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
