# handlers/qibla_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from math import sin, cos, atan2, degrees, radians

router = Router()

# Qibla qidirish holati
class QiblaState(StatesGroup):
    waiting_for_location = State()

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
async def process_qibla_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # State ni o'rnatamiz
    await state.set_state(QiblaState.waiting_for_location)
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Жойлашувни юбориш", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Eski xabarni o'chirish
    try:
        await callback.message.delete()
    except:
        pass
        
    await callback.message.answer(
        "🕋 <b>Қибла йўналишини аниқлаш</b>\n\n"
        "Сиз турган жойга кўра Қиблани аниқ ҳисоблаш учун, илтимос, пастдаги тугма орқали <b>жойлашувингизни (GPS)</b> юборинг.",
        reply_markup=kb,
        parse_mode="HTML"
    )

@router.message(F.location, QiblaState.waiting_for_location)
async def handle_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    angle = calculate_qibla(lat, lon)
    dynamic_url = f"https://ruslanyootuber-ux.github.io/insta-bot/?qibla={angle:.2f}"

    await state.clear() # Xotirani tozalash

    # 1. Klaviaturani yashirish uchun vaqtincha xabar yuborib, darhol o'chiramiz
    temp_msg = await message.answer("...", reply_markup=ReplyKeyboardRemove())
    
    try:
        await temp_msg.delete()
    except:
        pass

    builder = InlineKeyboardBuilder()
    builder.button(text="✨ 🧭 ЖОНЛИ КОМПАСНИ ОЧИШ 🧭 ✨", web_app=WebAppInfo(url=dynamic_url))
    builder.button(text="⬅️ Асосий Меню", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "✅ <b>Жойлашув муваффақиятли қабул қилинди!</b>\n\n"
        f"📍 Сизнинг координатангизга асосан Қибла бурчаги: <code>{angle:.2f}°</code>\n\n"
        "Пастдаги тугмани босинг va <b>Жонли компас</b> орқали Қиблани топинг!"
    )

    # 2. Asosiy natijani yuboramiz
    await message.answer(text=text, reply_markup=builder.as_markup(), parse_mode="HTML")
