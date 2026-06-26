import time
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.tasbeh_kb import get_tasbeh_keyboard
from data.tasbeh_data import TASBEH_ZIKRLARI

router = Router()
user_tasbeh = {}

@router.callback_query(F.data == "menu_tasbeh")
async def start_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_tasbeh[user_id] = {"count": 0, "index": 0, "last_click": 0}
    await callback.message.edit_text(
        f"📿 <b>Elektron Tasbeh</b>\n\nZikr: <b>{TASBEH_ZIKRLARI[0]['name']}</b>",
        reply_markup=get_tasbeh_keyboard(0, 0)
    )
    await callback.answer()

@router.callback_query(F.data == "count_tasbeh")
async def count_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    now = time.time()
    
    # Tez bosishdan himoya (0.5 soniya cheklov)
    if user_id in user_tasbeh and (now - user_tasbeh[user_id].get("last_click", 0) < 0.5):
        await callback.answer("❗ Juda tez bosmang!", show_alert=True)
        return

    user_tasbeh[user_id]["last_click"] = now
    
    # 33 marta bosilganda zikrni almashtirish
    user_tasbeh[user_id]["count"] += 1
    if user_tasbeh[user_id]["count"] >= 33:
        user_tasbeh[user_id]["count"] = 0
        user_tasbeh[user_id]["index"] = (user_tasbeh[user_id]["index"] + 1) % len(TASBEH_ZIKRLARI)
        await callback.answer("✅ Zikr almashtirildi!", show_alert=True)

    data = user_tasbeh[user_id]
    await callback.message.edit_reply_markup(reply_markup=get_tasbeh_keyboard(data["count"], data["index"]))
    await callback.answer(str(data["count"]))