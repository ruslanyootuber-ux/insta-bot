import os
import asyncio
import time
from instagrapi import Client

# 1. Instagram bilan ishlash qismi
async def instagram_worker():
    session_id = os.getenv("SESSION_ID")
    cl = Client()
    cl.login_by_sessionid(session_id)
    
    while True:
        print("Instagram vazifalari bajarilmoqda...")
        # BU YERGA INSTAGRAM KODLARINGIZNI YOZASIZ
        
        print("Instagram 5 daqiqa dam olmoqda...")
        await asyncio.sleep(300) # 300 soniya = 5 daqiqa

# 2. Serverni "tirik" saqlovchi hiyla (Keep-Alive)
async def keep_alive():
    while True:
        print("Server ishlamoqda...")
        await asyncio.sleep(60) # Har 60 soniyada log berib turadi

# Asosiy funksiya
async def main():
    # Ikkala funksiyani bir vaqtda ishga tushiramiz
    await asyncio.gather(instagram_worker(), keep_alive())

if __name__ == "__main__":
    print("Bot ishga tushdi!")
    asyncio.run(main())
