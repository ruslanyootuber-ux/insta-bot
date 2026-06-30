# utils/db.py

# Hozircha bazani oddiy lug'at (dictionary) shaklida qilamiz, 
# keyinchalik buni SQL bazaga o'tkazish juda oson.

# Foydalanuvchilar hududini saqlash uchun lug'at
user_regions = {}

async def get_user_region(user_id: int):
    """Foydalanuvchi hududini bazadan olish"""
    return user_regions.get(user_id, "Toshkent") # Hudud tanlanmagan bo'lsa, standart "Toshkent"

async def set_user_region(user_id: int, region: str):
    """Foydalanuvchi hududini bazaga yozish"""
    user_regions[user_id] = region
