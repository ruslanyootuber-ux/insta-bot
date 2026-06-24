import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

# Muhit o'zgaruvchilaridan ma'lumotlarni olish
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("STRING_SESSION")
target_user = "@Doktorgolivud"  # Kimga yozish kerakligi

# Tasodifiy xabarlar ro'yxati
messages = [
    "Salom, nima gaplar?",
    "Qalaysiz?",
    "Bugungi kun qanday o'tmoqda?",
    "Ishlar yaxshimi?",
    "Nimalar bilan bandsiz?"
]

async def main():
    # StringSession yordamida mijozni ishga tushirish
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    
    await client.start()
    print("Userbot muvaffaqiyatli ishga tushdi va ulanish o'rnatildi!")

    while True:
        try:
            msg = random.choice(messages)
            await client.send_message(target_user, msg)
            print(f"Xabar yuborildi: {target_user} -> {msg}")
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
        
        # 2 daqiqa (120 soniya) kutish
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
