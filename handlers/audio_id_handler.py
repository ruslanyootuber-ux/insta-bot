# handlers/audio_id_handler.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

# АДМИН ИД рақамингизни шу ерга ёзиб қўйинг (масалан: 12345678)
ADMIN_ID = 8727877170  

@router.message(F.audio)
async def get_audio_file_id(message: Message):
    """Агар аудио юборилса, унинг Telegram File ID сини қайтаради"""
    if message.from_user.id != ADMIN_ID:
        return # Админ бўлмаса, ҳеч нарса қилмайди

    audio_id = message.audio.file_id
    audio_name = message.audio.file_name or "Номсиз аудио"
    
    response_text = (
        f"🎵 <b>Аудио файл қабул қилинди!</b>\n\n"
        f"<b>Номи:</b> {audio_name}\n"
        f"<b>Код учун File ID:</b>\n"
        f"<code>{audio_id}</code>\n\n"
        f"<i>Ушбу ИД ни нусхалаб, suralar_data.py ичидаги тегишли суранинг 'audio_id' қисмига қўйинг.</i>"
    )
    
    await message.reply(text=response_text, parse_mode="HTML")
