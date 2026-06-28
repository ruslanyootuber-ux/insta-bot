from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from data.taxorat_data import TAHORAT_STEPS
from keyboards.taxorat_kb import get_taxorat_step_kb

router = Router()

@router.callback_query(F.data.startswith("taxorat_"))
async def show_taxorat_step(callback: CallbackQuery):
    # Фақат қадам индексини оламиз (масалан: taxorat_0)
    step_idx = int(callback.data.split("_")[1])
    
    if step_idx >= len(TAHORAT_STEPS) or step_idx < 0:
        await callback.answer("Бошқа қадам йўқ", show_alert=True)
        return

    step_data = TAHORAT_STEPS[step_idx]
    text = step_data["text"]
    gif_id = step_data["gif_id"]
    
    kb = get_taxorat_step_kb(step_idx, len(TAHORAT_STEPS))

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

# GIF ID аниқлагич ўзгаришсиз қолади
@router.message(F.animation)
async def get_gif_file_id(message: Message):
    gif_id = message.animation.file_id
    await message.reply(f"Сизи юборган GIF ID:\n\n<code>{gif_id}</code>", parse_mode="HTML")
