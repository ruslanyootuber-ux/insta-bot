import asyncio
import os
import requests
from aiogram import Bot

# Konfiguratsiya
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@namozvaqti1111p"
bot = Bot(token=BOT_TOKEN)

def get_namoz_vaqtlari():
    try:
        url = "https://islomapi.uz/api/present/day?region=Toshkent"
        response = requests.get(url, timeout=10).json()
        
        # Javobni tekshiramiz
        if 'times' not in response:
            return f"API dan ma'lumot noto'g'ri keldi: {response}"
            
        v = response['times']
        text = (f"🕋 *Namoz vaqtlari ({response['date']})*\n"
                f"📍 *Mintaqa: {response['region']}*\n\n"
                f"🌅 Tong: {v['tong_saharlik']}\n"
                f"☀️ Quyosh: {v['quyosh']}\n"
                f"🏙 Peshin: {v['peshin']}\n"
                f"🌇 Asr: {v['asr']}\n"
                f"🌆 Shom: {v['shom_iftor']}\n"
                f"🌙 Xufton: {v['hufton']}")
        return text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

async def main():
    while True:
        try:
            namoz_text = get_namoz_vaqtlari()
            await bot.send_message(chat_id=CHANNEL_ID, text=namoz_text, parse_mode="Markdown")
            await asyncio.sleep(10800) # 3 soat
        except Exception as e:
            print(f"Loop xatosi: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
