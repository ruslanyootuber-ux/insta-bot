from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS
from urllib.parse import quote

# !!! DIQQAT !!!
# BU YERGA O'Z BOTINGIZNING USERNAME'INI "@" BELGISISIZ YOZING
BOT_USERNAME = "NamozTaqvimi_Uz_Bot" 

# ASOSIY MENYU
def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🕌 Namoz vaqtlari", callback_data="menu_regions")
    builder.button(text="✨ Allohning 99 ismi", callback_data="menu_asmaul")
    builder.button(text="📿 Elektron tasbeh", callback_data="menu_tasbeh")
    builder.button(text="🤲 Kunlik duolar", callback_data="menu_duo")
    builder.button(text="📖 Kunlik hadis", callback_data="menu_hadis")
    builder.button(text="🕋 Qiblani topish", callback_data="menu_qibla")
    builder.button(text="🤲 Kunlik zikrlar", callback_data="menu_zikr_main")
    builder.button(text="🌙 Ramazon taqvimi", callback_data="menu_ramadan")
    builder.button(text="🔔 Eslatma belgilash", callback_data="menu_reminder")
    builder.button(text="☪️ Mazhabni tanlash", callback_data="menu_settings")
    builder.button(text="👨‍💻 Bog'lanish", callback_data="menu_creator")
    builder.button(text="⭐ Botni baholash", callback_data="menu_rate")

    # Guruhga qo'shish
    add_to_group_url = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    builder.row(InlineKeyboardButton(text="➕ Guruhga qo'shish", url=add_to_group_url))
    
    # Do'stlarga ulashish (URL kodlangan)
    share_text = "🕌 «Foydali Namoz Vaqtlari» boti — cho‘ntagingizdagi ishonchli yordamchi! 📱📿"
    encoded_text = quote(share_text)
    share_url = f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME}&text={encoded_text}"
    builder.row(InlineKeyboardButton(text="📲 Do'stlarga ulashish", url=share_url))

    # Tugmalar joylashuvi
    builder.adjust(2, 2, 2, 2, 2, 2, 1, 1) 
    return builder.as_markup()

# VILOYATLAR MENYUSI
def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in UZB_REGIONS.keys():
        builder.button(text=f"📍 {region}", callback_data=RegionCallback(region_name=region))
    
    builder.row(InlineKeyboardButton(text="⬅️ Bosh menyuga qaytish", callback_data="back_to_main"))
    builder.adjust(2) 
    return builder.as_markup()

# TUMANLAR MENYUSI
def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for district in UZB_REGIONS.get(region_name, []):
        builder.button(text=f"🏢 {district}", callback_data=DistrictCallback(district_name=district))
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    builder.adjust(2) 
    return builder.as_markup()