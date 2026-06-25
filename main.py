import asyncio
import random
import datetime
from telethon import TelegramClient, functions

# Konfiguratsiyalar
API_ID = ... 
API_HASH = '...'
STRING_SESSION = '...'

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

TEXTS = ["Salom hammaga! Kanalimda kutaman, u yerda hamma narsa erkinroq, kiring o‘zingiz ko‘rasiz... 🍑🔥",
"Yolg‘izlik jonimga tegdi... Kanalim profilimda, kirsangiz pushaymon bo‘lmaysiz, kutyapman. 💦🫦",
"Bu yerda hamma ko‘radi, kanalimda esa sirli... Linkim profilimda, kiring kutib qolaman. 🍌💋",
"Sizga ko‘rsatadigan narsalarim juda ko‘p, kanalim profilimda. Kiring, birga bo‘lamiz. 😉🔥",
"Zerikib qoldim, kanalimga o‘ting, u yerda sizga atab maxsus narsalar bor. 🍓🤤",
"Kanalim profilimda, kiring va o‘zingizni erkin his qiling. Kutaman, shoshiling... 🍑💦",
"Men bilan yaqinroq tanishishni istaysizmi? Unda kanalimga o‘ting, havolasi profilimda. 🫦🔥",
"Bu yerda gaplashib bo‘lmaydi... Kanalimda kutyapman, kiring, juda qiziq bo‘ladi. 🍌✨",
"Sizni sog‘indim... Kanalim profilimda, kiring, sog‘inchimizni tarqataylik. 🍓🍑",
"Juda erkalashni xohlayman, kanalim profilimda. Kiring, kutyapman... 💋💦",
"Hamma sirlarim kanalimda, profilim orqali kiring. Sizni kutib qolaman. 🔥🔞",
"Juda ehtirosli va qiziq, kanalim profilimda. Kiring, birga vaqt o‘tkazamiz. 🍌🫦",
"Kirib ko‘ring, afsuslanmaysiz. Kanalim profilimda, kutaman... 🍑💦",
"Siz bilan yaqinroq bo‘lish uchun kanalimga kiring, havolasi profilimda. 🔥🍓",
"Kelib kayfiyatimni ko‘tarib yuboring, kanalim profilimda, kutaman... 💋🍌",
"Juda qizib ketdim, kanalimda kutyapman. Linki profilimda... 🫦🔥",
"O‘zingizni erkin his qiladigan joy – kanalimda. Profilim orqali kiring. 🍑💦",
"Sog‘inchimni bosishga yordam bering, kanalim profilimda. Kutaman... 🍓💋",
"Hammasini ko‘rsataman, kanalim profilimda. Shoshiling, kutaman... 🍌🔥",
"Meni toping, kanalim profilimda. U yerda kutib qolaman... 🫦✨",
"Juda issiq xabarlarim bor, kanalim profilimda. Kirib o‘qing... 🍑💦",
"Men bilan bo‘lishga tayyormisiz? Kanalim profilimda, kutaman. 🍌🔞",
"Kanalimga kiring, u yerda erkinroqmiz. Linki profilimda, kutyapman. 🍓🫦",
"Sizni kutib charchadim, kanalim profilimda, kiring... 🔥🍑",
"Eng qiziq narsalar kanalimda, profilim orqali o‘ting. 💦💋",
"Birga vaqt o‘tkazishni istaysizmi? Kanalim profilimda, kutaman... 🍌✨",
"Juda ehtirosli sirlarim bor, kanalim profilimda. Kiring... 🍑🔥",
"Sog‘indim, kanalimga o‘ting, profilimda linki. Kutaman... 🫦🍓",
"Bu yerda gapirish uyat, kanalimda esa bemalol. Profilimga kiring. 🍌💦",
"Sizni kutib qolaman, kanalim profilimda. Shoshiling... 🔥💋",
"Juda qiziq, kanalimga o‘ting, linki profilimda. 🍑✨",
"Men bilan tanishishni istasangiz, kanalim profilimda, kiring... 🫦🍌",
"Juda ochilib gaplashamiz, kanalim profilimda, kuting... 🍓💦",
"Meni toping, kanalim profilimda. Kutaman, jonim... 🔥🫦",
"Qiziq narsalarim ko‘p, kanalim profilimda. Kiring... 🍌🍑",
"Sizni kutaman, kanalim profilimda. Kelmaysizmi? 🍓✨",
"Juda erkinman, kanalimda ko‘rasiz. Profilimga o‘ting... 💋💦",
"Ehtirosli va qiziq, kanalim profilimda, kiring... 🍌🔥",
"Men bilan yaqin bo‘ling, kanalim profilimda. Kutyapman... 🫦🍑",
"Juda sog‘indim, kanalim profilimda. Kiring, shoshiling... 🍓💦",
"Hammadann yashirincha... Kanalim profilimda, kiring... 💋🍌",
"Juda issiq, kanalim profilimda, kiring... 🔥🍑",
"Sizni kutaman, kanalim profilimda. Kiring, xo‘pmi? 🫦✨",
"Juda qiziqarli, kanalim profilimda, o‘tib ko‘ring... 🍓🍌",
"Men bilan vaqt o‘tkazing, kanalim profilimda... 💦🔥",
"Juda ehtirosliman, kanalim profilimda, kiring... 🍑💋",
"Sizni sog‘inib kutyapman, kanalim profilimda... 🫦🍌",
"Kirib ko‘ring, kanalim profilimda, kutaman... ✨🍓",
"Juda erkinmiz, kanalim profilimda. Kiring... 🔥💦",
"Meni toping, kanalim profilimda. Kutib qolaman! 🍌🍑",
] # 50+ matn

async def get_groups():
    """Siz a'zo bo'lgan guruhlarni avtomatik aniqlash"""
    groups = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            groups.append(dialog)
    return groups

async def human_logic():
    while True:
        # 00:00 - 06:00 oralig'ida uxlash
        now = datetime.datetime.now().hour
        if 0 <= now < 6:
            await asyncio.sleep(3600)
            continue

        groups = await get_groups()
        random.shuffle(groups) # Guruhlar tartibini aralashtirish

        for group in groups:
            try:
                # Insondek mantiq: xabar yozishdan oldin oxirgi xabarni olish
                messages = await client.get_messages(group, limit=1)
                
                if messages and random.choice([True, False]):
                    await messages[0].reply(random.choice(TEXTS))
                else:
                    await client.send_message(group, random.choice(TEXTS))
                
                # Insondek pauza: har bir guruhdan keyin 10-15 daqiqa kutish
                wait_time = random.randint(600, 900) 
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                print(f"Xatolik: {e}")
                continue

async def main():
    await client.start()
    print("Userbot insondek ishlash rejimida ishga tushdi...")
    await human_logic()

if __name__ == '__main__':
    client.loop.run_until_complete(main())