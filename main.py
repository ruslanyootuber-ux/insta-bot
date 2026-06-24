import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

# --- ON/OFF TUGMASI ---
# Shu yerga "OFF" deb yozsangiz, bot ishlashni to'xtatadi
BOT_STATUS = "OFF" 
# ----------------------

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

async def sender_worker(client):
    while True:
        msg = random.choice(messages)
        await client.send_message(target_user, msg)
        print(f"Xabar yuborildi: {msg}")
        await asyncio.sleep(120)

async def heart_beat():
    while True:
        await asyncio.sleep(10)

async def main():
    if BOT_STATUS.upper() == "OFF":
        print("Bot o'chirilgan (OFF holatda). Server kutish rejimida...")
        while True:
            await asyncio.sleep(3600) # Bot o'chirilgan bo'lsa, resurs ishlatmay uxlab turadi

    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.start()
    print("Userbot ishga tushdi!")
    
    await asyncio.gather(sender_worker(client), heart_beat())

if __name__ == "__main__":
    asyncio.run(main())