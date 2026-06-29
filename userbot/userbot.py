import asyncio
import random
from telethon import TelegramClient, events

# API ma'lumotlaringiz
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
session_str = 'YOUR_SESSION_STRING'

client = TelegramClient(StringSession(session_str), api_id, api_hash)

# Reklama qilinadigan guruhlar ro'yxati
target_groups = ['group_username1', 'group_username2', 'group_username3']

# Qiziqarli Islomiy reklamalar ro'yxati
ads = [
    "✨ Assalomu alaykum! Namoz — dinning ustuni. Namoz vaqtlari va tartibini o'rganishda yordam beradigan botimizga marhamat: @namoz_bot_username",
    "🌙 Namozga befarq bo'lmang! Har kunlik namozlaringizni o'z vaqtida o'qish uchun ajoyib ko'makchi: @namoz_bot_username",
    "🤲 Namoz — Alloh bilan muloqotdir. Botimiz orqali namoz o'qishni mukammal o'rganing: @namoz_bot_username"
]

async def advertiser():
    while True:
        try:
            for group in target_groups:
                # Reklama yuborish
                msg = random.choice(ads)
                await client.send_message(group, msg)
                print(f"Xabar yuborildi: {group}")
                
                # Tasodifiy reply qismi (har doim ham emas, 30% ehtimollik bilan)
                if random.random() < 0.3:
                    # Guruhdagi oxirgi xabarga reply qilish
                    async for message in client.iter_messages(group, limit=1):
                        await message.reply("To'g'ri aytasiz, namoz eng muhimi! 🕌")
                
                # Har bir yuborish orasida biroz kutish (spam cheklovini kamaytirish uchun)
                await asyncio.sleep(60) 
            
            # 5 daqiqalik sikl
            await asyncio.sleep(240)
        except Exception as e:
            print(f"Xatolik: {e}")
            await asyncio.sleep(60)

# Userbotni ishga tushirish
async def main():
    await client.start()
    await advertiser()

if __name__ == '__main__':
    asyncio.run(main())
