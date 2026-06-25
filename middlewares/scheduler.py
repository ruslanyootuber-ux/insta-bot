from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot, db
from utils.aladhan_api import get_prayer_times

async def send_daily_reminders():
    # Bazadagi barcha foydalanuvchilarni olamiz
    users = db.get_all_users() # Buni db.py ga qo'shishimiz kerak
    
    for user in users:
        user_id, district = user[0], user[2]
        if district:
            times = await get_prayer_times(district)
            # Bu yerda mantiq: Agar hozirgi vaqt namoz vaqtiga yaqin bo'lsa, xabar yuborish
            await bot.send_message(user_id, f"🕌 <b>{district}</b> uchun namoz vaqti yaqinlashdi...")
