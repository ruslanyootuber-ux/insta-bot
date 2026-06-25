import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Konfiguratsiyalar
API_ID = int(os.getenv("API_ID", 0)) # Default qiymat qo'shildi
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

async def perform_login():
    """Raqam va kodni so'rab, sessiya kodini qaytaruvchi funksiya"""
    print("\n--- 🔐 TELEGRAM AUTHENTICATION ---")
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        phone = input("📱 Telefon raqamingizni kiriting (+998xxxxxxxxx): ")
        await client.send_code_request(phone)
        code = input("📩 Kodni kiriting: ")
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return None
            
        new_session = client.session.save()
        print(f"\n✅ Muvaffaqiyatli! Sizning SESSION_STRINGingiz:")
        print(f"\n{new_session}\n")
        print("Buni nusxalab, Fly.io secrets ga SESSION_STRING qilib saqlang.")
        return new_session
    return None

async def main():
    # Agar sessiya string bo'lmasa, login so'raydi
    if not SESSION_STRING:
        await perform_login()
        return # Yangi login bo'lsa, skriptni qayta ishga tushirish kerak

    # Asosiy client
    client = TelegramClient(
        StringSession(SESSION_STRING), 
        API_ID, 
        API_HASH,
        device_model="PC 64-bit",
        system_version="Windows 11",
        app_version="Desktop 5.0.1"
    )

    await client.start()
    print("🚀 Userbot serverda ishga tushdi va Telegram hisobini boshqarmoqda...")
    
    # Bu yerda o'z vazifalaringizni bajaring
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())