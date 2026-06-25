from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from loader import bot, db
from utils.aladhan_api import get_prayer_times

router = Router()

# --- 1. Avtomatik eslatma tekshiruvi (Scheduler buni har 1 daqiqada chaqiradi) ---
async def check_and_send_reminders():
    users = db.get_all_users() # (user_id, full_name, district, reminder_time, school)
    current_time = datetime.now().strftime("%H:%M")
    
    for user in users:
        # Bazadagi ustunlar: 0:id, 1:name, 2:district, 3:reminder_time, 4:school
        user_id, district, reminder_time = user[0], user[2], user[3]
        
        if reminder_time and reminder_time > 0 and district:
            times = await get_prayer_times(district)
            if not times: continue
            
            for prayer, p_time in times.items():
                try:
                    prayer_dt = datetime.strptime(p_time, "%H:%M")
                    remind_dt = (prayer_dt - timedelta(minutes=reminder_time)).strftime("%H:%M")
                    
                    if current_time == remind_dt:
                        await bot.send_message(
                            user_id, 
                            f"🔔 <b>Eslatma:</b> {reminder_time} daqiqadan so'ng <b>{prayer}</b> vaqti kiradi!"
                        )
                except:
                    continue

# --- 2. Eslatma sozlamalari ---
def get_reminder_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="15 daqiqa oldin", callback_data="remind_15")
    builder.button(text="30 daqiqa oldin", callback_data="remind_30")
    builder.button(text="❌ Eslatmani o'chirish", callback_data="remind_0")
    builder.button(text="⬅️ Orqaga", callback_data="back_to_menu")
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

# --- 3. Mazhab sozlamalari ---
@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🕌 Mazhab: Hanafi", callback_data="set_school_0")
    builder.button(text="🕋 Mazhab: Shafi'i", callback_data="set_school_1")
    builder.button(text="⬅️ Orqaga", callback_data="back_to_menu")
    builder.adjust(1)
    await callback.message.edit_text(
        "⚙️ <b>Sozlamalar</b>\n\n"
        "O'zingizga mos mazhabni tanlang (Asr vaqti uchun):",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("set_school_"))
async def set_school(callback: CallbackQuery):
    school = int(callback.data.split("_")[2])
    db.update_school(callback.from_user.id, school)
    msg = "✅ Hanafi mazhabi tanlandi." if school == 0 else "✅ Shafi'i mazhabi tanlandi."
    await callback.answer(msg, show_alert=True)