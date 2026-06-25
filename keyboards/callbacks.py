from aiogram.filters.callback_data import CallbackData

# Viloyatlar uchun maxsus callback
class RegionCallback(CallbackData, prefix="reg"):
    region_name: str

# Tumanlar uchun maxsus callback
class DistrictCallback(CallbackData, prefix="dist"):
    district_name: str
