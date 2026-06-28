# handlers/tasbeh_handlers.py

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
        reply_markup=get_tasbeh_keyboard(0, 0),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "count_tasbeh")
async def count_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    now = time.time()

    if user_id in user_tasbeh and (now - user_tasbeh[user_id].get("last_click", 0) < 0.3):
        await callback.answer("❗ Juda tez bosmang!", show_alert=True)
        return

    user_tasbeh[user_id]["last_click"] = now

    user_tasbeh[user_id]["count"] += 1
    if user_tasbeh[user_id]["count"] >= 33:
        user_tasbeh[user_id]["count"] = 0
        user_tasbeh[user_id]["index"] = (user_tasbeh[user_id]["index"] + 1) % len(TASBEH_ZIKRLARI)
        await callback.answer("✅ 33 ga yetdi, zikr almashtirildi!", show_alert=True)

    data = user_tasbeh[user_id]
    await callback.message.edit_text(
        f"📿 <b>Elektron Tasbeh</b>\n\nZikr: <b>{TASBEH_ZIKRLARI[data['index']]['name']}</b>",
        reply_markup=get_tasbeh_keyboard(data["count"], data["index"]),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "reset_tasbeh")
async def reset_tasbeh(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_tasbeh:
        user_tasbeh[user_id]["count"] = 0
        await callback.message.edit_text(
            f"📿 <b>Elektron Tasbeh</b>\n\nZikr: <b>{TASBEH_ZIKRLARI[user_tasbeh[user_id]['index']]['name']}</b>",
            reply_markup=get_tasbeh_keyboard(0, user_tasbeh[user_id]["index"]),
            parse_mode="HTML"
        )
    await callback.answer("🔄 Sanoq nollandi!", show_alert=False)

@router.callback_query(F.data == "change_zikr")
async def change_zikr_manual(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_tasbeh:
        user_tasbeh[user_id]["index"] = (user_tasbeh[user_id]["index"] + 1) % len(TASBEH_ZIKRLARI)
        user_tasbeh[user_id]["count"] = 0
        await callback.message.edit_text(
            f"📿 <b>Elektron Tasbeh</b>\n\nZikr: <b>{TASBEH_ZIKRLARI[user_tasbeh[user_id]['index']]['name']}</b>",
            reply_markup=get_tasbeh_keyboard(0, user_tasbeh[user_id]["index"]),
            parse_mode="HTML"
        )
    await callback.answer("Zikr o'zgardi")
