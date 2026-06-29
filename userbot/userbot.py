import asyncio
import random
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# Muhit o'zgaruvchilari
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_str = os.getenv("SESSION_STRING")

client = TelegramClient(StringSession(session_str), api_id, api_hash)

ads = [
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

target_groups = ['Qiziqarli_testlar_tanishuvlar', 'Marhamat_mfy', 'bardankolmahallagruppasi'] # Guruhlar username'lari

async def advertiser():
    while True:
        try:
            for group in target_groups:
                msg = random.choice(ads)
                await client.send_message(group, msg)
                
                # Reply qilish ehtimoli (30%)
                if random.random() < 0.3:
                    async for message in client.iter_messages(group, limit=1):
                        await message.reply("Barakalloh, judayam foydali ma'lumotlar!")
                
                await asyncio.sleep(60) # Har bir yuborish orasida kutish
            
            await asyncio.sleep(240) # Sikl uchun qolgan vaqt (jami 5 daqiqa)
        except Exception as e:
            print(f"Xatolik: {e}")
            await asyncio.sleep(60)
