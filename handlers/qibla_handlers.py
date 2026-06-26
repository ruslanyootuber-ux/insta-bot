from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from math import sin, cos, atan2, degrees, radians

router = Router()

# Makkai Mukarramaning koordinatalari
MAKKAH_LAT = 21.422487
MAKKAH_LON = 39.826206

def calculate_qibla(lat, lon):
    phi1, lambda1 = radians(lat), radians(lon)
    phi2, lambda2 = radians(MAKKAH_LAT), radians(MAKKAH_LON)
    
    y = sin(lambda2 - lambda1) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(lambda2 - lambda1)
    
    qibla = degrees(atan2(y, x))
    return (qibla + 360) % 360

@router.callback_query(F.data == "menu_qibla")
async def process_qibla(callback: CallbackQuery):
    await callback.message.edit_text(
        "📍 <b>Qibla yo'nalishini aniqlash</b>\n\n"
        "Iltimos, joylashuvingizni (location) yuboring, shunda men sizga "
        "Qibla tomonini aniqlab beraman.",
    )

@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    qibla_angle = calculate_qibla(lat, lon)
    
    await message.answer(
        f"🕋 <b>Qibla yo'nalishi:</b> {qibla_angle:.2f}°\n\n"
        f"Kompas yordamida telefoningizni ushbu gradusga to'g'rilang."
    )
