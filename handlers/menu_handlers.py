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
from loader import db 

router = Router()

async def get_live_prayer_text(user_id):
    try:
        region = db.get_district(user_id)
        times = await get_prayer_times(region)
        if times and "next_prayer" in times:
            return f"⏰ Navbatdagi: <b>{times['next_prayer']}</b>"
    except Exception:
        pass
    return "⏰ Namoz vaqtlari yuklanmoqda..."

# =====================================================================
# PREMIUM SUB-MENYULAR
# =====================================================================

@router.callback_query(F.data.startswith("submenu_"))
async def open_submenus(callback: CallbackQuery):
    user_id = callback.from_user.id
    live_info = await get_live_prayer_text(user_id)
    
    data_map = {
        "submenu_ibodat": ("🟢 <b>Ибодат масалалари</b>", get_ibodat_menu_kb()),
        "submenu_ilm": ("📖 <b>Илм ва Зикр бурчаги</b>", get_ilm_menu_kb()),
        "submenu_taqvim": ("🗺️ <b>Намоз ва Тақвим</b>", get_taqvim_menu_kb()),
        "submenu_sozlamalar": ("⚙️ <b>Созламалар ва Алоқа</b>", get_sozlamalar_menu_kb()),
    }

    if callback.data in data_map:
        header, keyboard = data_map[callback.data]
        text = f"{header}\n\n{live_info}\n\nKerakli bo'limni tanlang:"
        await callback.message.edit_text(text=text, reply_markup=keyboard, parse_mode="HTML")
    
    await callback.answer()

# =====================================================================
# ASOSIY VA HUDUD MENYULARI
# =====================================================================

@router.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: CallbackQuery):
    live_info = await get_live_prayer_text(callback.from_user.id)
    text = f"<b>Bosh menyu</b>\n\n{live_info}\n\n<i>Kerakli bo'limni tanlang:</i>"
    await callback.message.edit_text(text=text, reply_markup=get_main_menu_kb(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back_to_regions")
async def back_to_menu_regions(callback: CallbackQuery):
    await callback.message.edit_text("📍 <b>Viloyatni tanlang:</b>", reply_markup=get_regions_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(RegionCallback.filter())
async def process_region_selection(callback: CallbackQuery, callback_data: RegionCallback):
    region_name = callback_data.region_name
    db.update_district(callback.from_user.id, region_name)
    await callback.message.edit_text(f"📍 <b>{region_name}</b> tanlandi.\n\n🏙 Endi tumanni tanlang:", 
                                     reply_markup=get_districts_keyboard(region_name), parse_mode="HTML")
    await callback.answer()

@router.callback_query(DistrictCallback.filter())
async def process_district_selection(callback: CallbackQuery, callback_data: DistrictCallback):
    district_name = callback_data.district_name
    db.update_district(callback.from_user.id, district_name)
    
    await callback.message.edit_text("⏳ <i>Namoz vaqtlari yuklanmoqda...</i>", parse_mode="HTML")
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
    await callback.answer()
