from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from keyboards.callbacks import RegionCallback, DistrictCallback
from utils.locations import UZB_REGIONS

def get_regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Barcha viloyatlarni tugma qilib chiqaramiz
    for region in UZB_REGIONS.keys():
        builder.button(
            text=f"📍 {region}",
            callback_data=RegionCallback(region_name=region)
        )
        
    # Tugmalarni 2 tadan qilib joylashtiramiz (chiroyli dizayn)
    builder.adjust(2)
    return builder.as_markup()

def get_districts_keyboard(region_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Tanlangan viloyatning tumanlarini olamiz
    districts = UZB_REGIONS.get(region_name, [])
    
    for district in districts:
        builder.button(
            text=f"🏢 {district}",
            callback_data=DistrictCallback(district_name=district)
        )
    
    # Orqaga qaytish tugmasini alohida qo'shamiz
    builder.button(text="⬅️ Viloyatlarga qaytish", callback_data="back_to_regions")
    
    # Tumanlarni 2 tadan qilib, eng oxiridagi "Orqaga" tugmasini 1 ta qilib joylashtirish
    # Buning uchun oxirgi qatorga 1 beramiz
    sizes = [2] * (len(districts) // 2) + ([1] if len(districts) % 2 != 0 else []) + [1]
    builder.adjust(*sizes)
    
    return builder.as_markup()
