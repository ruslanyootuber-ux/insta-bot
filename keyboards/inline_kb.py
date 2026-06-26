from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS

# ASOSIY MENYU (Ekranning yarmini egallaydi)
def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🕌 Namoz vaqtlari", callback_data="menu_regions")
    builder.button(text="✨ Asmaul Husna", callback_data="menu_asmaul")
    builder.button(text="📿 Elektron tasbeh", callback_data="menu_tasbeh")
    builder.button(text="🤲 Kunlik duolar", callback_data="menu_duo")
    builder.button(text="📖 Kunlik hadis", callback_data="menu_hadis")
    builder.button(text="🕋 Qiblani topish", callback_data="menu_qibla")
    builder.button(text="🤲 Kunlik zikrlar", callback_data="menu_zikr_main")
    builder.button(text="🌙 Ramazon taqvimi", callback_data="menu_ramadan")
    builder.button(text="🔔 Eslatma belgilash", callback_data="menu_reminder")
    builder.button(text=" ☪️ Mazhabni tanlash", callback_data="menu_settings")
    builder.button(text="👨‍💻 Bog'lanish", callback_data="menu_creator")
    builder.button(text="⭐ Botni baholash", callback_data="menu_rate")

    builder.adjust(2) # 2 ta ustun, ixcham va chiroyli
    return builder.as_markup()

# VILOYATLAR MENYUSI (Faqat Namoz vaqtini bosganda chiqadi)
def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in UZB_REGIONS.keys():
        builder.button(text=f"📍 {region}", callback_data=RegionCallback(region_name=region))
    
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyuga qaytish", callback_data="back_to_main"))
    builder.adjust(2) 
    return builder.as_markup()

# TUMANLAR MENYUSI (O'zgarishsiz qolaveradi)
def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for district in UZB_REGIONS.get(region_name, []):
        builder.button(text=f"🏢 {district}", callback_data=DistrictCallback(district_name=district))
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    builder.adjust(2) 
    return builder.as_markup()