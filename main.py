import asyncio
import os
import requests
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@namozvaqti1111"
bot = Bot(token=BOT_TOKEN)

def get_namoz_vaqtlari():
    try:
        url = "https://api.aladhan.com/v1/timingsByCity?city=Tashkent&country=Uzbekistan&method=3"
        response = requests.get(url, timeout=10).json()
        
        data = response['data']['timings']
        date = response['data']['date']['readable']
        
        # Markdown belgilarisiz oddiy matn
        text = (f"🕋 Namoz vaqtlari ({date})\n"
                f"📍 Toshkent\n\n"
                f"🌅 Tong (Fajr): {data['Fajr']}\n"
                f"☀️ Quyosh (Sunrise): {data['Sunrise']}\n"
                f"🏙 Peshin (Dhuhr): {data['Dhuhr']}\n"
                f"🌇 Asr (Asr): {data['Asr']}\n"
                f"🌆 Shom (Maghrib): {data['Maghrib']}\n"
                f"🌙 Xufton (Isha): {data['Isha']}")
        return text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

async def main():
    while True:
        try:
            namoz_text = get_namoz_vaqtlari()
            # parse_mode ni olib tashladik, shunda xatolik bermaydi
            await bot.send_message(chat_id=CHANNEL_ID, text=namoz_text)
            await asyncio.sleep(10800) 
        except Exception as e:
            print(f"Loop xatosi: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
