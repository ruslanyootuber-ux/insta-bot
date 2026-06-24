import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("STRING_SESSION")
target_user = "@Doktorgolivud"

messages = [
    "Salom, nima gaplar?",
    "Qalaysiz?",
    "Bugungi kun qanday o'tmoqda?",
    "Ishlar yaxshimi?",
    "Nimalar bilan bandsiz?"
]

# 1-vazifa: Xabar yuborish
async def sender_worker(client):
    while True:
        msg = random.choice(messages)
        await client.send_message(target_user, msg)
        print(f"Xabar yuborildi: {msg}")
        await asyncio.sleep(120) # 2 daqiqa

# 2-vazifa: Serverni "tirik" ushlab turish
async def heart_beat():
    while True:
        await asyncio.sleep(10) # Har 10 soniyada "men ishlayapman" deb turadi

async def main():
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.start()
    print("Userbot ishga tushdi!")
    
    # Ikkala vazifani bir vaqtda yurgizamiz
    await asyncio.gather(sender_worker(client), heart_beat())

if __name__ == "__main__":
    asyncio.run(main())
