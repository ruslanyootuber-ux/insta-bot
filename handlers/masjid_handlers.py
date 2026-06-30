# handlers/masjid_handlers.py

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline_kb import get_location_keyboard

router = Router()

# Masjid qidirish uchun holat
class MasjidState(StatesGroup):
    waiting_for_location = State()

# 1. Foydalanuvchi "Masjidlar va Manzillar" tugmasini bosganda
@router.callback_query(F.data == "menu_find_masjid")
async def ask_location_for_masjid(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Holatni o'rnatamiz
    await state.set_state(MasjidState.waiting_for_location)
    
    # Xabarni yuboramiz
    await callback.message.answer(
        text="📌 <b>Yaqin atrofdagi masjidlarni topish uchun:</b>\n\n"
             "Pastdagi <code>📍 Joylashuvni yuborish</code> tugmasini bosing.\n\n"
             "<i>(Agar tugma chiqmasa, yozish maydonchasi yonidagi tugmachani bosing)</i>",
        reply_markup=get_location_keyboard(),
        parse_mode="HTML"
    )

# 2. Lokatsiya kelganda, FAQATGINA "MasjidState" kutilayotgan bo'lsa ishlaydi
@router.message(F.location, MasjidState.waiting_for_location)
async def process_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    # Ish bitgach, bot xotirasini tozalaymiz
    await state.clear()

    # Reply klaviaturani yashiramiz
    await message.answer("⏳ <i>Joylashuv qabul qilindi, xaritalar tayyorlanmoqda...</i>", 
                         reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")

    yandex_url = f"https://yandex.com/maps/?text=masjid&ll={lon},{lat}&z=14"
    google_url = f"https://www.google.com/maps/search/masjid/@{lat},{lon},14z"

    builder = InlineKeyboardBuilder()
    builder.button(text="🗺️ Yandex Maps orqali ochish", url=yandex_url)
    builder.button(text="🌐 Google Maps orqali ochish", url=google_url)
    builder.button(text="⬅️ Asosiy menyuga qaytish", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "✨ <b>Joylashuv muvaffaqiyatli aniqlandi!</b>\n\n"
        "Atrofingizdagi jome masjidlarini ko'rish va ulargacha bo'lgan eng yaqin yo'lni chizish uchun "
        "quyidagi xaritalardan birini tanlang 👇"
    )

    await message.answer(
        text=text, 
        reply_markup=builder.as_markup(), 
        parse_mode="HTML"
    )
