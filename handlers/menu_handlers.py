# handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from keyboards.callbacks import RegionCallback, DistrictCallback
from keyboards.inline_kb import (
    get_regions_keyboard, 
    get_districts_keyboard, 
    get_main_menu_kb,
    get_ibodat_menu_kb,
    get_ilm_menu_kb,
    get_taqvim_menu_kb,
    get_sozlamalar_menu_kb
)
from utils.alahdan_api import get_prayer_times
from loader import db # Baza obyektini import qilamiz

router = Router()

# Jonli vaqtni hisoblovchi yordamchi funksiya
async def get_live_prayer_text(user_id):
    region = db.get_district(user_id)
    times = await get_prayer_times(region)
    if times and "next_prayer" in times:
        return f"⏰ Navbatdagi: <b>{times['next_prayer']}</b>"
    return "⏰ Namoz vaqtlari yuklanmoqda..."

# =====================================================================
# PREMIUM SUB-MENYULAR
# =====================================================================

@router.callback_query(F.data.startswith("submenu_"))
async def open_submenus(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    live_info = await get_live_prayer_text(user_id)
    
    data = callback.data
    text = ""
    reply_kb = None
    
    if data == "submenu_ibodat":
        text = f"🟢 <b>Ибодат масалалари</b>\n\n{live_info}\n\nKerakli mavzuni tanlang:"
        reply_kb = get_ibodat_menu_kb()
    elif data == "submenu_ilm":
        text = f"📖 <b>Илм ва Зикр бурчаги</b>\n\n{live_info}\n\nKerakli bo'limni tanlang:"
        reply_kb = get_ilm_menu_kb()
    elif data == "submenu_taqvim":
        text = f"🗺️ <b>Намоз ва Тақвим</b>\n\n{live_info}\n\nKerakli bo'limni tanlang:"
        reply_kb = get_taqvim_menu_kb()
    elif data == "submenu_sozlamalar":
        text = f"⚙️ <b>Созламалар ва Алоқа</b>\n\n{live_info}\n\nKerakli bo'limni tanlang:"
        reply_kb = get_sozlamalar_menu_kb()
        
    if text:
        await callback.message.edit_text(text=text, reply_markup=reply_kb, parse_mode="HTML")

# =====================================================================
# ASOSIY VA HUDUD MENYULARI
# =====================================================================

@router.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: CallbackQuery):
    await callback.answer()
    live_info = await get_live_prayer_text(callback.from_user.id)
    text = (f"<b>Bosh menyu</b>\n\n{live_info}\n\n<i>Kerakli bo'limni tanlang:</i>")
    await callback.message.edit_text(text=text, reply_markup=get_main_menu_kb(), parse_mode="HTML")

@router.callback_query(F.data == "back_to_regions")
async def back_to_menu_regions(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📍 <b>Viloyatni tanlang:</b>", reply_markup=get_regions_keyboard(), parse_mode="HTML")

@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    await callback.answer()
    region_name = callback_data.region_name
    # Hududni bazaga saqlab qo'yamiz
    db.update_district(callback.from_user.id, region_name)
    await callback.message.edit_text(f"📍 <b>{region_name}</b> tanlandi.\n\n🏙 Endi tumanni tanlang:", 
                                     reply_markup=get_districts_keyboard(region_name), parse_mode="HTML")

@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    await callback.answer()
    district_name = callback_data.district_name
    db.update_district(callback.from_user.id, district_name) # Tumanni bazaga saqlash
    
    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yangilanmoqda...</i>", parse_mode="HTML")
    times = await get_prayer_times(district_name)

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    builder.button(text="🏠 Asosiy menu", callback_data="back_to_main")
    builder.adjust(1)

    if times:
        today = datetime.now().strftime("%d.%m.%Y")
        text = (f"🕌 <b>{district_name}</b> uchun namoz vaqtlari:\n📅 Sana: {today}\n\n"
                f"🌅 <b>Bomdod:</b> {times['Bomdod']}\n☀️ <b>Peshin:</b> {times['Peshin']}\n"
                f"🌤 <b>Asr:</b> {times['Asr']}\n🌇 <b>Shom:</b> {times['Shom']}\n"
                f"🌌 <b>Xufton:</b> {times['Xufton']}")
    else:
        text = "❌ Xatolik yuz berdi."
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
