import asyncio
import random
from telethon import TelegramClient

# 1. Sozlamalar (Bularni Fly.io Secrets'ga qo'shing!)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("STRING_SESSION")
target_user = "@Doktorgolivud" # Kimga yozish kerakligi

# Xabarlar ro'yxati
messages = [
    "Salom, nima gaplar?😌",
    "Qalaysiz?😁",
    "Bugungi kun qanday o'tmoqda?🤒",
    "Tushlik qildingizmi?💆",
    "Yangi yangiliklar bormi?🐓"
]

async def main():
    client = TelegramClient(None, api_id, api_hash)
    
    # Session string orqali ulanish
    await client.start(session=session_string)
    print("Userbot ishga tushdi!")

    while True:
        try:
            msg = random.choice(messages)
            await client.send_message(target_user, msg)
            print(f"Xabar yuborildi: {msg}")
        except Exception as e:
            print(f"Xatolik: {e}")
        
        # 2 daqiqa (120 soniya) kutish
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
