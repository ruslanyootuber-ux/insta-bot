# handlers/extra_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta
from loader import bot
from utils.aladhan_api import get_prayer_times

router = Router()

# --- 1. Avtomatik eslatma tekshiruvi ---
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
                        await bot.send_message(
                            user_id, 
                            f"🔔 <b>Eslatma:</b> {reminder_time} daqiqadan so'ng <b>{prayer}</b> vaqti kiradi!",
                            parse_mode="HTML"
                        )
                except:
                    continue

# --- 2. Eslatma sozlamalari ---
def get_reminder_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="15 daqiqa oldin", callback_data="remind_15")
    builder.button(text="30 daqiqa oldin", callback_data="remind_30")
    builder.button(text="❌ Eslatmani o'chirish", callback_data="remind_0")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main") # <-- back_to_main га ўзгарди
    builder.adjust(1)
    return builder.as_markup()

@router.callback_query(F.data == "menu_reminder")
async def process_reminder(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🔔 <b>Eslatma sozlamalari</b>\n\nNamoz vaqti kirishidan qancha oldin ogohlantirishni tanlang:", 
        reply_markup=get_reminder_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("remind_"))
async def set_reminder(callback: CallbackQuery):
    time = int(callback.data.split("_")[1])
    db.update_reminder(callback.from_user.id, time)
    await callback.answer(f"✅ Eslatma {time} daqiqaga o'rnatildi!" if time > 0 else "❌ Eslatma o'chirildi.", show_alert=True)

# --- 3. Mazhab sozlamalari ---
@router.callback_query(F.data == "menu_settings")
async def process_settings(callback: CallbackQuery):
    await callback.answer()
    builder = InlineKeyboardBuilder()
    builder.button(text="🕌 Mazhab: Hanafi", callback_data="set_school_0")
    builder.button(text="🕋 Mazhab: Shafi'i", callback_data="set_school_1")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main") # <-- back_to_main га ўзгарди
    builder.adjust(1)
    await callback.message.edit_text(
        "⚙️ <b>Sozlamalar</b>\n\nO'zingizga mos mazhabni tanlang:", 
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("set_school_"))
async def set_school(callback: CallbackQuery):
    school = int(callback.data.split("_")[2])
    db.update_school(callback.from_user.id, school)
    await callback.answer("✅ Mazhab saqlandi.", show_alert=True)

# --- 4. Yaratuvchi bo'limi ---
@router.callback_query(F.data == "menu_creator")
async def process_creator(callback: CallbackQuery):
    await callback.answer()
    text = (
        "👨‍💻 <b>Bot Yaratuvchisi</b>\n\n"
        "Barcha viloyat va tumanlar uchun eng aniq namoz vaqtlari yetkazib berish maqsad qilingan.\n\n"
        "📩 <i>Taklif va murojaatlar uchun pastdagi ‹Admin bilan bog'lanish› tugmasini bosing:</i>"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Admin bilan bog'lanish", url="https://t.me/mrxruslann")
    builder.button(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main") # <-- back_to_main га ўзгарди
    builder.adjust(1) 
    await callback.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")

# --- 5. Baholash (Reyting) bo'limi ---
async def show_rating_menu(message):
    avg_rating, total_voters = db.get_rating_stats()
    
    full_stars_count = int(avg_rating)
    empty_stars_count = 5 - full_stars_count
    star_visual = "⭐" * full_stars_count + "🤍" * empty_stars_count
    
    percentage = int((avg_rating / 5) * 100) if total_voters > 0 else 0
    
    text = (
        "⭐ <b>Botni baholash</b>\n\n"
        f"📊 <b>Umumiy reyting:</b> {avg_rating} / 5.0\n"
        f"🌟 <b>Ko'rsatkich:</b> {star_visual} ({percentage}%)\n"
        f"👥 <b>Ovoz berganlar:</b> {total_voters} ta\n\n"
        "<i>Sizning fikringiz biz uchun muhim! Iltimos, quyidagi yulduzchalardan birini tanlab botga baho bering:</i>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="1 ⭐", callback_data="rate_1")
    builder.button(text="2 ⭐", callback_data="rate_2")
    builder.button(text="3 ⭐", callback_data="rate_3")
    builder.button(text="4 ⭐", callback_data="rate_4")
    builder.button(text="5 ⭐", callback_data="rate_5")
    builder.adjust(5) 
    
    builder.row(InlineKeyboardButton(text="⬅️ Бош менюга қайтиш", callback_data="back_to_main")) # <-- back_to_main га ўзгарди
    
    try:
        await message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception:
        pass

@router.callback_query(F.data == "menu_rate")
async def process_rate_menu(callback: CallbackQuery):
    await callback.answer()
    await show_rating_menu(callback.message)

@router.callback_query(F.data.startswith("rate_"))
async def process_rating_vote(callback: CallbackQuery):
    rating = int(callback.data.split("_")[1])
    db.update_rating(callback.from_user.id, rating)
    await callback.answer(f"🎉 Siz botga {rating} yulduz baho berdingiz. Rahmat!", show_alert=True)
    await show_rating_menu(callback.message)
