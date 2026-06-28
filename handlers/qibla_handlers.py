# handlers/qibla_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
    await callback.answer()
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Асосий меню", callback_data="back_to_main")

    text = (
        "🕋 <b>Қибла йўналишини аниқлаш</b>\n\n"
        "Жойлашувингизга кўра Каъба томонни аниқлаб бериш учун "
        "пастдаги тугма ёки Телеграм менюси орқали <b>Локация (Location)</b> юборинг.\n\n"
        "<i>📌 Эслатма: Тўғри ўлчаш учун телефонингиз геолокацияси (GPS) ёқилган бўлиши керак.</i>"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@router.message(F.location)
async def handle_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude

    qibla_angle = calculate_qibla(lat, lon)

    # Орқага қайтиш тугмаси
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Бош менюга", callback_data="back_to_main")

    # Градусга қараб йўналиш кўрсаткичини танлаш (Шимолга нисбатан)
    # Масалан: 240° учун Шимоли-Ғарб кўрсаткичи
    direction_arrow = "🧭"
    if 337.5 <= qibla_angle < 360 or 0 <= qibla_angle < 22.5:
        direction_arrow = "⬆️ (Шимол)"
    elif 22.5 <= qibla_angle < 67.5:
        direction_arrow = "↗️ (Шимоли-Шарқ)"
    elif 67.5 <= qibla_angle < 112.5:
        direction_arrow = "➡️ (Шарқ)"
    elif 112.5 <= qibla_angle < 157.5:
        direction_arrow = "↘️ (Жануби-Шарқ)"
    elif 157.5 <= qibla_angle < 202.5:
        direction_arrow = "⬇️ (Жануб)"
    elif 202.5 <= qibla_angle < 247.5:
        direction_arrow = "↙️ (Жануби-Ғарб)"
    elif 247.5 <= qibla_angle < 292.5:
        direction_arrow = "⬅️ (Ғарб)"
    elif 292.5 <= qibla_angle < 337.5:
        direction_arrow = "↖️ (Шимоли-Ғарб)"

    text = (
        "✨ <b>Қибла йўналиши муваффақиятли аниқланди!</b> ✨\n\n"
        f"🕋 <b>Қибла бурчаги:</b> <code>{qibla_angle:.2f}°</code>\n"
        f"🧭 <b>Тахминий йўналиш:</b> {direction_arrow}\n\n"
        "📖 <b>Қандай тўғриланилади?</b>\n"
        "1. Телефонингизда <b>Компас (Compass)</b> дастурини очинг.\n"
        "2. Телефонни ерга параллел (текис) ҳолатда ушланг.\n"
        f"3. Телефон тепа қисмини айнан <b>{qibla_angle:.0f}°</b> градусга бургунингизча айланинг.\n"
        "4. Кўрсаткич шу рақамга келганда, телефонингиз тўғри <b>Каъбаи Муаззамага</b> қараган бўлади.\n\n"
        "<i>⚠️ Диққат! Телефонингиз яқинида темир жисмлар ёки магнитли ғилофлар бўлмаслигига ишонч ҳосил қилинг, акс ҳолда компас нотўғри кўрсатиши мумкин.</i>"
    )

    await message.answer(
        text=text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
