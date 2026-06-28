# handlers/erkaklar_namozi_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from data.erkaklar_namozi_data import ERKAKLAR_NAMOZI_STEPS
from keyboards.erkaklar_namozi_kb import get_erkaklar_namozi_step_kb

router = Router()

@router.callback_query(F.data.startswith("erkaklar_namozi_"))
async def show_erkaklar_namozi_step(callback: CallbackQuery):
    step_idx = int(callback.data.split("_")[2]) # "erkaklar_namozi_X" бўлгани учун 2-индексни оламиз

    if step_idx >= len(ERKAKLAR_NAMOZI_STEPS) or step_idx < 0:
        await callback.answer("Бошқа қадам йўқ", show_alert=True)
        return

    step_data = ERKAKLAR_NAMOZI_STEPS[step_idx]
    text = step_data["text"]
    gif_id = step_data["gif_id"]

    kb = get_erkaklar_namozi_step_kb(step_idx, len(ERKAKLAR_NAMOZI_STEPS))

    await callback.message.delete()

    try:
        await callback.message.answer_animation(
            animation=gif_id, 
            caption=text, 
            reply_markup=kb, 
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text=f"{text}\n\n<i>(GIF ҳали юкланмаган)</i>", 
            reply_markup=kb, 
            parse_mode="HTML"
        )

    await callback.answer()
@router.message(F.animation)
async def get_gif_file_id(message: Message):
    """Фойдаланувчи ГИФ юборганда унинг file_id сини қайтаради"""
    gif_id = message.animation.file_id
    await message.reply(
        text=f"<b>Сурат/ГИФ ИД рақами:</b>\n\n<code>{gif_id}</code>\n\n"
             f"Ушбу кодни нусхалаб, taxorat_data.py файлидаги тегишли жойга қўйинг.",
        parse_mode="HTML"
    )