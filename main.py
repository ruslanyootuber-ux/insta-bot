import asyncio
import random
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# Muhit o'zgaruvchilari
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("STRING_SESSION")
target_user = "@Doktorgolivud" 

async def main():
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    await client.start()
    print("Userbot ishga tushdi!")

    try:
        while True:
            # Har 2 daqiqada xabar
            await client.send_message(target_user, "Salom, qalay ahvol?")
            print(f"Xabar yuborildi: {target_user}")
            await asyncio.sleep(120)
    except asyncio.CancelledError:
        # Fly.io to'xtatish signali yuborganda bu qism ishlaydi
        print("Bot xatosiz to'xtatilmoqda...")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
