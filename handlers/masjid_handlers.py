# handlers/masjid_handlers.py

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.inline_kb import get_location_keyboard, get_main_menu_kb

router = Router()

# 1. Foydalanuvchi "Masjidga yo'l" tugmasini bosganda
@router.callback_query(F.data == "menu_find_masjid")
async def ask_location_for_masjid(callback: CallbackQuery):
    await callback.answer()
    
    try:
        # Eski inline menyuli xabarni o'chirib yuboramiz (chalkashlik bo'lmasligi uchun)
        await callback.message.delete()
    except Exception as e:
        logging.error(f"Xabarni o'chirishda xatolik: {e}")

    # Joylashuv so'raydigan Reply tugmani yuboramiz
    await callback.message.answer(
        text="📌 <b>Yaqin atrofdagi masjidlarni topish uchun:</b>\n\n"
             "Pastdagi <code>📍 Joylashuvni yuborish</code> tugmasini bosing.\n\n"
             "<i>(Agar tugma chiqmasa, yozish maydonchasi yonidagi tugmachani bosing)</i>",
        reply_markup=get_location_keyboard(),
        parse_mode="HTML"
    )

# 2. Foydalanuvchi geolokatsiyani yuborganida uni tutib olish
@router.message(F.location)
async def process_location(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude

    # 1-QADAM: Avval pastdagi qotib qoladigan klaviaturani o'chirib yuboruvchi qisqa xabar jo'natamiz
    xabar = await message.answer(
        text="⏳ <i>Joylashuv qabul qilindi, xaritalar tayyorlanmoqda...</i>", 
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

    # 2-QADAM: Yandex va Google xaritalari uchun koordinata bo'yicha masjid qidirish linklari
    yandex_url = f"https://yandex.com/maps/?text=masjid&ll={lon},{lat}&z=14"
    google_url = f"https://www.google.com/maps/search/masjid/@{lat},{lon},14z"

    builder = InlineKeyboardBuilder()
    builder.button(text="🗺️ Yandex Maps orqali ochish", url=yandex_url)
    builder.button(text="🌐 Google Maps orqali ochish", url=google_url)
    builder.button(text="⬅️ Asosiy menyuga qaytish", callback_data="back_to_main")
    builder.adjust(1)

    text = (
        "✨ <b>Joylashuv muvaffaqiyatli aniqlandi!</b>\n\n"
        "Atrofingizdagi jome masjidlarini ko'rish va ulargacha bo'lgan eng yaqin yo'lni (marshrut) chizish uchun "
        "quyidagi xaritalardan birini tanlang 👇"
    )

    # 3-QADAM: Endi bemalol Inline tugmali xabarni yuboramiz
    await message.answer(
        text=text, 
        reply_markup=builder.as_markup(), 
        parse_mode="HTML"
    )
    
    # (Qo'shimcha): Boyagi "kutib turing" degan qisqa xabarni o'chirib yuboramiz, chiroyli turishi uchun
    try:
        await xabar.delete()
    except:
        pass
