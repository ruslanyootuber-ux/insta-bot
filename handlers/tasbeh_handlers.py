from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.tasbeh_kb import get_tasbeh_keyboard
from data.zikr_data import ZIKRLAR

router = Router()

# Foydalanuvchi ma'lumotlarini saqlash
user_data = {}

@router.callback_query(F.data == "menu_tasbeh") # Aynan "menu_tasbeh"
async def start_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data[user_id] = {"count": 0, "zikr_index": 0}
    
    text = f"📿 <b>Elektron Tasbeh</b>\n\nTanlangan zikr: <b>{ZIKRLAR[0]['name']}</b>\n\nSanoqni boshlash uchun tugmani bosing."
    await callback.message.edit_text(text, reply_markup=get_tasbeh_keyboard(0, 0))

@router.callback_query(F.data == "count_zikr")
async def count_zikr(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"count": 0, "zikr_index": 0}
    
    user_data[user_id]["count"] += 1
    data = user_data[user_id]
    
    # Tugmani yangilash (sanoq raqami bilan)
    await callback.message.edit_reply_markup(
        reply_markup=get_tasbeh_keyboard(data["count"], data["zikr_index"])
    )
    await callback.answer(f"{data['count']}")