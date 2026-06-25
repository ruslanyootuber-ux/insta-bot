import os
import asyncio
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Konfiguratsiya
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Video yuklash funksiyasi
async def download_instagram_video(url, chat_id):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{chat_id}.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f'video_{chat_id}.mp4'

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salom! Instagram havolasini yuboring.")

@dp.message(F.text.contains("instagram.com"))
async def handle_insta_link(message: types.Message):
    await message.answer("Video yuklanmoqda, kuting...")
    try:
        video_path = await download_instagram_video(message.text, message.chat.id)
        # 3.x versiyada FSInputFile ishlatiladi
        video = FSInputFile(video_path)
        await message.answer_video(video=video)
        os.remove(video_path)
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
