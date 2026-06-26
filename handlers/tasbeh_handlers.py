from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.tasbeh_kb import get_tasbeh_keyboard
from data.tasbeh_data import TASBEH_ZIKRLARI

router = Router()
user_tasbeh = {}

@router.callback_query(F.data == "menu_tasbeh")
async def start_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_tasbeh[user_id] = {"count": 0, "index": 0}
    
    text = f"📿 <b>Elektron Tasbeh</b>\n\nZikr: <b>{TASBEH_ZIKRLARI[0]['name']}</b>\n\nSanoqni boshlash uchun tugmani bosing."
    await callback.message.edit_text(text, reply_markup=get_tasbeh_keyboard(0, 0))

@router.callback_query(F.data == "count_tasbeh")
async def count_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_tasbeh:
        user_tasbeh[user_id] = {"count": 0, "index": 0}
    
    user_tasbeh[user_id]["count"] += 1
    data = user_tasbeh[user_id]
    
    await callback.message.edit_reply_markup(
        reply_markup=get_tasbeh_keyboard(data["count"], data["index"])
    )
    await callback.answer(f"{data['count']}")
