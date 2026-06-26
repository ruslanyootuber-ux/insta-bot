from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS

def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # 1. Viloyatlar tugmalari
    for region in UZB_REGIONS.keys():
        builder.button(
            text=f"📍 {region}",
            callback_data=RegionCallback(region_name=region)
        )
    
    # 2. Asosiy menyu tugmalari
    bot_username = "Bshsudhdhdj_bot"
    
    builder.button(text="✨ Asmaul Husna", callback_data="menu_asmaul")
    builder.button(text="📿 Elektron Tasbeh", callback_data="menu_tasbeh")
    builder.button(text="🤲 Duolar", callback_data="menu_duo")
    builder.button(text="📖 Kun hadisi", callback_data="menu_hadis")
    builder.button(text="🕋 Qibla yo'nalishi", callback_data="menu_qibla")
    builder.button(text="🤲 Tonggi va Kechki zikrlar", callback_data="menu_zikr_main")
    builder.button(text="🌙 Ramazon taqvimi", callback_data="menu_ramadan")
    builder.button(text="🔔 Eslatma", callback_data="menu_reminder")
    builder.button(text="⚙️ Sozlamalar", callback_data="menu_settings")
    builder.button(text="👨‍💻 Yaratuvchi", callback_data="menu_creator")
    builder.button(text="⭐ Baholash", callback_data="menu_rate")

    # 3. Tashqi havolalar
    builder.row(InlineKeyboardButton(
        text="➕ Botni guruhga qo'shish", 
        url=f"https://t.me/{bot_username}?startgroup=true"
    ))
    builder.row(InlineKeyboardButton(
        text="↗️ Do'stlarga ulashish", 
        url=f"https://t.me/share/url?url=https://t.me/{bot_username}&text=🕌 Barcha viloyat va tumanlar uchun eng aniq namoz vaqtlari boti!"
    ))

    # Barcha tugmalarni 2 tadan qilib tartiblaydi
    builder.adjust(2) 

    return builder.as_markup()

def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    districts = UZB_REGIONS.get(region_name, [])

    for district in districts:
        builder.button(
            text=f"🏢 {district}",
            callback_data=DistrictCallback(district_name=district)
        )

    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    builder.adjust(2) 

    return builder.as_markup()