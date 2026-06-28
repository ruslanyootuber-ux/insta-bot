# handlers/media_handlers.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.animation)
async def get_gif_file_id(message: Message):
    """Ботга ГИФ юборилганда унинг узун file_id кодини қайтаради"""
    gif_id = message.animation.file_id
    await message.reply(
        text=f"<b>🎬 ГИФ ИД рақами аниқланди:</b>\n\n"
             f"<code>{gif_id}</code>\n\n"
             f"<i>Ушбу кодни нусхалаб, керакли маълумотлар базаси (data) файлига қўйишингиз мумкин.</i>",
        parse_mode="HTML"
    )
