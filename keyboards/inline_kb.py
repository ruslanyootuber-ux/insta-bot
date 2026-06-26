from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS

def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # 1. Viloyatlar tugmalari (2 tadan joylashadi)
    for region in UZB_REGIONS.keys():
        builder.button(
            text=f"📍 {region}",
            callback_data=RegionCallback(region_name=region)
        )
    builder.adjust(2) # Viloyatlarni 2 qatorga bo'lamiz
    
    # 2. Rang-barang va zamonaviy qo'shimcha tugmalar
    bot_username = "Bshsudhdhdj_bot"
        # ... viloyatlar tsiklidan keyin
    
    # Yangi Zikrlar tugmasi (Katta, alohida qatorda)
    builder.row(
        InlineKeyboardButton(text="🤲 Tonggi va Kechki zikrlar", callback_data="menu_zikr_main")
    )
    
    # Eslatma va Sozlamalar (1-qator)
    builder.row(
        InlineKeyboardButton(text="🔔 Eslatma", callback_data="menu_reminder"),
        # ... qolgan kodlar o'zgarishsiz

    # Eslatma va Sozlamalar (1-qator)
    builder.row(
        InlineKeyboardButton(text="🔔 Eslatma (Tez kunda)", callback_data="menu_reminder"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="menu_settings")
    )
    
    # Yaratuvchi va Baholash (2-qator)
    builder.row(
        InlineKeyboardButton(text="👨‍💻 Yaratuvchi", callback_data="menu_creator"),
        InlineKeyboardButton(text="⭐ Baholash", callback_data="menu_rate")
    )
    
    # Guruhga qo'shish (3-qator, katta uzun tugma)
    builder.row(
        InlineKeyboardButton(
            text="➕ Botni guruhga qo'shish", 
            url=f"https://t.me/{bot_username}?startgroup=true"
        )
    )
    
    # Do'stlarga ulashish (4-qator, katta uzun tugma)
    builder.row(
        InlineKeyboardButton(
            text="↗️ Do'stlarga ulashish", 
            url=f"https://t.me/share/url?url=https://t.me/{bot_username}&text=🕌 Barcha viloyat va tumanlar uchun eng aniq namoz vaqtlari boti! Siz ham foydalanib ko'ring."
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
    sizes = [2] * (len(districts) // 2) + ([1] if len(districts) % 2 != 0 else []) + [1]
    builder.adjust(*sizes)
    
    return builder.as_markup()