import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Video sifatini aniqlash va yuklash
async def download_instagram_video(url, chat_id):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{chat_id}.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f'video_{chat_id}.mp4'

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Salom! Instagram havolasini yuboring, men uni sizga yuklab beraman.")

@dp.message_handler()
async def process_link(message: types.Message):
    if "instagram.com" in message.text:
        await message.answer("Video tahlil qilinmoqda...")
        try:
            # Video yuklash
            video_path = await download_instagram_video(message.text, message.chat.id)
            await message.answer_video(open(video_path, 'rb'))
            # Ishlatilgandan so'ng faylni o'chirish
            os.remove(video_path)
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {e}")
    else:
        await message.answer("Iltimos, to'g'ri Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp)
