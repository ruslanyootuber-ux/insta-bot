from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from loader import bot, db
from utils.aladhan_api import get_prayer_times
from keyboards.inline_kb import get_regions_keyboard

router = Router()

# --- 1. Orqaga qaytish funksiyasi ---
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    text = "👇 <i>Iltimos, o'zingizga kerakli viloyatni tanlang:</i>"
    await callback.message.edit_text(text=text, reply_markup=get_regions_keyboard())

# --- 2. Avtomatik eslatma tekshiruvi ---
async def check_and_send_reminders():
    users = db.get_all_users()
    current_time = datetime.now().strftime("%H:%M")
    
    for user in users:
        user_id, district, reminder_time = user[0], user[2], user[3]
        if reminder_time and reminder_time > 0 and district:
            times = await get_prayer_times(district)
            if not times: continue
            
            for prayer, p_time in times.items():
                try:
                    prayer_dt = datetime.strptime(p_time, "%H:%M")
                    remind_dt = (prayer_dt - timedelta(minutes=reminder_time)).strftime("%H:%M")
                    if current_time == remind_dt:
                        await bot.send_message(user_id, f"🔔 <b>Eslatma:</b> {reminder_time} daqiqadan so'ng <b>{prayer}</b> vaqti kiradi!")
                except:
                    continue

# --- 3. Eslatma sozlamalari ---
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
    await callback.answer()
    await callback.message.edit_text("🔔 <b>Eslatma sozlamalari</b>\n\nNamoz vaqti kirishidan qancha oldin ogohlantirishni tanlang:", reply_markup=get_reminder_keyboard())

@router.callback_query(F.data.startswith("remind_"))
async def set_reminder(callback: CallbackQuery):
    time = int(callback.data.split("_")[1])
    db.update_reminder(callback.from_user.id, time)
    await callback.answer(f"✅ Eslatma {time} daqiqaga o'rnatildi!" if time > 0 else "❌ Eslatma o'chirildi.", show_alert=True)

# --- 4. Mazhab sozlamalari ---
@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="🕌 Mazhab: Hanafi", callback_data="set_school_0")
    builder.button(text="🕋 Mazhab: Shafi'i", callback_data="set_school_1")
    builder.button(text="⬅️ Orqaga", callback_data="back_to_menu")
    builder.adjust(1)
    await callback.message.edit_text("⚙️ <b>Sozlamalar</b>\n\nO'zingizga mos mazhabni tanlang:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("set_school_"))
async def set_school(callback: CallbackQuery):
    school = int(callback.data.split("_")[2])
    db.update_school(callback.from_user.id, school)
    await callback.answer("✅ Mazhab saqlandi.", show_alert=True)