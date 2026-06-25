from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import bot, db

router = Router()

def get_reminder_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="15 daqiqa oldin", callback_data="remind_15")
    builder.button(text="30 daqiqa oldin", callback_data="remind_30")
    builder.button(text="❌ Eslatmani o'chirish", callback_data="remind_0")
    builder.adjust(1)
    return builder.as_markup()

@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔔 <b>Eslatma sozlamalari</b>\n\n"
        "Namoz vaqti kirishidan qancha oldin ogohlantirishni tanlang:",
        reply_markup=get_reminder_keyboard()
    )

@router.callback_query(F.data.startswith("remind_"))
async def set_reminder(callback: CallbackQuery):
    time = int(callback.data.split("_")[1])
    db.update_reminder(callback.from_user.id, time)
    
    msg = f"✅ Eslatma {time} daqiqaga o'rnatildi!" if time > 0 else "❌ Eslatma o'chirildi."
    await callback.answer(msg, show_alert=True)
    await callback.message.delete()