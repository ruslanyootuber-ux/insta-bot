import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Konfiguratsiyalar
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
BOT_TOKEN = os.getenv("BOT_TOKEN")  # BotFatherdan olingan token

# Bot client (token orqali ishlaydi)
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# User uchun vaqtinchalik xotira
temp_data = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Salom! Userbotni ishga tushirish uchun telefon raqamingizni yuboring (Format: +998xxxxxxxxx)")

@bot.on(events.NewMessage)
async def handler(event):
    chat_id = event.chat_id
    text = event.text

    # Telefon raqamni olish
    if chat_id not in temp_data:
        if text.startswith('+'):
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            sent = await client.send_code_request(text)
            temp_data[chat_id] = {'client': client, 'phone': text, 'phone_code_hash': sent.phone_code_hash}
            await event.respond("Raqam qabul qilindi. Kodni yuboring:")
    
    # Kodni olish va login qilish
    elif 'phone_code_hash' in temp_data[chat_id] and 'code' not in temp_data[chat_id]:
        try:
            client = temp_data[chat_id]['client']
            await client.sign_in(temp_data[chat_id]['phone'], text, phone_code_hash=temp_data[chat_id]['phone_code_hash'])
            session_string = client.session.save()
            await event.respond(f"✅ Muvaffaqiyatli! Sizning SESSION_STRINGingiz:\n\n`{session_string}`\n\nBuni Fly.io secrets ga saqlang.")
            await client.disconnect()
            del temp_data[chat_id]
        except Exception as e:
            await event.respond(f"❌ Xatolik: {e}")

async def main():
    # Agar SESSION_STRING bo'lsa, userbotni ishga tushir
    if SESSION_STRING:
        userbot = TelegramClient(
            StringSession(STRING_SESSION), 
            API_ID, 
            API_HASH,
            device_model="PC 64-bit",
            system_version="Windows 11",
            app_version="Desktop 5.0.1"
        )
        await userbot.start()
        print("🚀 Userbot serverda ishga tushdi va Telegram hisobini boshqarmoqda...")
        # Vazifalar shu yerda bo'ladi...
    
    print("🤖 Bot faol, telefon raqam va kodni kutmoqda...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
