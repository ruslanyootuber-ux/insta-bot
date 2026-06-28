# handlers/ayollar_namozi_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.ayollar_namozi_data import AYOLLAR_NAMOZI_STEPS
from keyboards.ayollar_namozi_kb import get_ayollar_namozi_step_kb

router = Router()

@router.callback_query(F.data.startswith("ayollar_namozi_"))
async def show_ayollar_namozi_step(callback: CallbackQuery):
    # Коллбекдан индексни ажратиб оламиз ("ayollar_namozi_X")
    step_idx = int(callback.data.split("_")[2])
    
    if step_idx >= len(AYOLLAR_NAMOZI_STEPS) or step_idx < 0:
        await callback.answer("Бошқа қадам йўқ", show_alert=True)
        return

    step_data = AYOLLAR_NAMOZI_STEPS[step_idx]
    text = step_data["text"]
    gif_id = step_data["gif_id"]
    
    kb = get_ayollar_namozi_step_kb(step_idx, len(AYOLLAR_NAMOZI_STEPS))

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
