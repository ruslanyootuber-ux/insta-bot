import asyncio
import os
import requests
from aiogram import Bot
from datetime import datetime

# Konfiguratsiya
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@namozvaqti1111p" # Kanal ID
bot = Bot(token=BOT_TOKEN)

def get_namoz_vaqtlari():
    # API orqali Toshkent vaqtlari (misol uchun)
    url = "https://islomapi.uz/api/present/day?region=Toshkent"
    response = requests.get(url).json()
    v = response['times']
    
    # Chiroyli tablitsa ko'rinishi
    text = (f"🕋 *Namoz vaqtlari ({response['date']})*\n"
            f"📍 *Mintaqa: {response['region']}*\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🌅 Tong:    {v['tong_saharlik']}\n"
            f"☀️ Quyosh:  {v['quyosh']}\n"
            f"🏙 Peshin:  {v['peshin']}\n"
            f"🌇 Asr:     {v['asr']}\n"
            f"🌆 Shom:    {v['shom_iftor']}\n"
            f"🌙 Xufton:  {v['hufton']}\n"
            f"━━━━━━━━━━━━━━━━━━")
    return text

async def main():
    while True:
        try:
            namoz_text = get_namoz_vaqtlari()
            await bot.send_message(chat_id=CHANNEL_ID, text=namoz_text, parse_mode="Markdown")
            # Har 3 soatda yangilash (yoki xohlagan vaqtingiz)
            await asyncio.sleep(10) 
        except Exception as e:
            print(f"Xatolik: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
