# handlers/audio_id_handler.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

# АДМИН ИД рақамингизни шу ерга ёзиб қўйинг (масалан: 12345678)
ADMIN_ID = 8727877170  

from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.audio)
async def get_audio_file_id(message: Message):
    audio_id = message.audio.file_id
    await message.reply(f"🎵 File ID: <code>{audio_id}</code>", parse_mode="HTML")
