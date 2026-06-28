from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from data.taxorat_data import TAHORAT_STEPS
from keyboards.taxorat_kb import get_taxorat_step_kb

router = Router()

@router.callback_query(F.data.startswith("taxorat_"))
async def show_taxorat_step(callback: CallbackQuery):
    # Callback ma'lumotini qismlarga ajratamiz (masalan: taxorat_0_latin)
    parts = callback.data.split("_")
    step_idx = int(parts[1])
    lang = parts[2]
    
    # Agar qadamlar tugagan bo'lsa
    if step_idx >= len(TAHORAT_STEPS) or step_idx < 0:
        await callback.answer("Boshqa qadam yo'q" if lang == 'latin' else "Бошқа қадам йўқ", show_alert=True)
        return

    # Kerakli qadam ma'lumotlarini olish
    step_data = TAHORAT_STEPS[step_idx]
    text = step_data["text_latin"] if lang == 'latin' else step_data["text_cyrillic"]
    gif_id = step_data["gif_id"]
    
    # Klaviaturani yasash
    kb = get_taxorat_step_kb(step_idx, len(TAHORAT_STEPS), lang)

    # Eski xabarni o'chirib, yangisini (GIF bilan) yuboramiz
    await callback.message.delete()
    
    try:
        # GIF va matnni yuborish
        await callback.message.answer_animation(
            animation=gif_id, 
            caption=text, 
            reply_markup=kb, 
            parse_mode="HTML"
        )
    except Exception:
        # Agar GIF ID xato bo'lsa yoki hali kiritilmagan bo'lsa, faqat matn ketadi
        await callback.message.answer(
            text=f"{text}\n\n<i>(GIF hali yuklanmagan)</i>", 
            reply_markup=kb, 
            parse_mode="HTML"
        )
        
    await callback.answer()
    # Buni handlers/taxorat_handlers.py faylining oxiriga qo'shing
@router.message(F.animation)
async def get_gif_file_id(message: Message):
    """Botga yuborilgan har qanday GIF'ning file_id'sini qaytaradi"""
    gif_id = message.animation.file_id
    await message.reply(f"Siz yuborgan GIF'ning ID'si:\n\n<code>{gif_id}</code>", parse_mode="HTML")