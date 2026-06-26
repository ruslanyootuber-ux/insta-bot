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
    builder.adjust(2) 

        # 2. Asosiy menyu tugmalari
    bot_username = "Bshsudhdhdj_bot"
    #99 ism tugmasi
    builder.row(InlineKeyboardButton(text="✨ Asmaul Husna", callback_data="menu_asmaul"))
    # Tasbeh tugmasi (Mana bu qator to'g'rilandi!)
    builder.row(InlineKeyboardButton(text="📿 Elektron Tasbeh", callback_data="menu_tasbeh"))

    # Hadis hikmatlar tugmasi
    builder.row(InlineKeyboardButton(text="📖 Kun hadisi", callback_data="menu_hadis"))
    #duo tugmasi
        #duo tugmasi
    builder.row(InlineKeyboardButton(text="🤲 Duolar", callback_data="menu_duo"))
    # Qibla tugmasi
    builder.row(InlineKeyboardButton(text="🕋 Qibla yo'nalishi", callback_data="menu_qibla"))


    # Zikrlar tugmasi
    builder.row(InlineKeyboardButton(text="🤲 Tonggi va Kechki zikrlar", callback_data="menu_zikr_main"))
    
    # Ramazon taqvimi tugmasi
    builder.row(InlineKeyboardButton(text="🌙 Ramazon taqvimi", callback_data="menu_ramadan"))

    # Eslatma va Sozlamalar
    builder.row(
        InlineKeyboardButton(text="🔔 Eslatma", callback_data="menu_reminder"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="menu_settings")
    )

    # Yaratuvchi va Baholash
    builder.row(
        InlineKeyboardButton(text="👨‍💻 Yaratuvchi", callback_data="menu_creator"),
        InlineKeyboardButton(text="⭐ Baholash", callback_data="menu_rate")
    )

    # Guruhga qo'shish
    builder.row(
        InlineKeyboardButton(
            text="➕ Botni guruhga qo'shish", 
            url=f"https://t.me/{bot_username}?startgroup=true"
        )
    )

    # Do'stlarga ulashish
    builder.row(
        InlineKeyboardButton(
            text="↗️ Do'stlarga ulashish", 
            url=f"https://t.me/share/url?url=https://t.me/{bot_username}&text=🕌 Barcha viloyat va tumanlar uchun eng aniq namoz vaqtlari boti!"
        )
    )

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

    # Tugmalarni tartiblash
    # sizes ro'yxatini to'g'ri hisoblash
    builder.adjust(2) 

    return builder.as_markup()