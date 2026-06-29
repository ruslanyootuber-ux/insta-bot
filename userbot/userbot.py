import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

# 10 ta xilma-xil reklama matnlari
ADS = [
    "✨ Assalomu alaykum! Namoz — dinning ustuni. Namoz vaqtlari va tartibini o'rganishda yordam beradigan botimiz: @bot_username",
    "🕌 Namoz o'qishni boshlamoqchimisiz? Botimiz sizga eng oson yo'llarni ko'rsatadi. Profilimga qarang!",
    "🌙 Har bir kunimiz namoz bilan go'zal! Namoz vaqtlarini o'tkazib yubormaslik uchun botimizdan foydalaning: @bot_username",
    "🤲 Namoz — Alloh bilan muloqot. Botimiz orqali namozni mukammal o'rganing. Batafsil botimizda!",
    "📖 Namozni qanday to'g'ri o'qishni bilasizmi? Bizning botimizda barcha ma'lumotlar bor. @bot_username ga kiring.",
    "💡 Namoz — iymonning nuri. Namozingizni o'z vaqtida o'qishga yordam beruvchi bot: @bot_username",
    "🕌 Botim orqali namoz vaqtlarini kuzatib boring! Profilimda batafsil ma'lumot qoldirganman.",
    "✨ Islomiy odoblar va namoz tartiblari! Botimiz bilan har bir kuningiz yanada mazmunli bo'ladi: @bot_username",
    "🤲 Namoz — najot! Namoz o'qishni endi boshlayotganlar uchun maxsus bot: @bot_username",
    "🌙 Namoz — qalblar shifosi. Botimizdan namoz vaqtlari va suralar haqida bilib oling! Profilimga o'ting."
]

TARGET_GROUPS = ['group_username1', 'group_username2'] # Guruhlar manzili

async def advertiser():
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    session_str = os.getenv("SESSION_STRING")

    if not api_id or not api_hash or not session_str:
        print("Xatolik: API ma'lumotlari topilmadi!")
        return

    client = TelegramClient(StringSession(session_str), int(api_id), api_hash)
    await client.start()
    print("Userbot muvaffaqiyatli ishga tushdi!")

    while True:
        try:
            for group in TARGET_GROUPS:
                msg = random.choice(ADS)
                await client.send_message(group, msg)
                
                # 30% ehtimollik bilan reply qilish
                if random.random() < 0.3:
                    async for message in client.iter_messages(group, limit=1):
                        await message.reply("To'g'ri aytasiz, namoz eng muhimi! 🕌")
                
                await asyncio.sleep(60) # Har bir xabar oralig'i
            
            await asyncio.sleep(240) # Sikl uchun pauza
        except Exception as e:
            print(f"Userbotda xatolik: {e}")
            await asyncio.sleep(60)
