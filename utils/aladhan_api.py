# utils/alahdan_api.py

import aiohttp
from datetime import datetime

async def get_prayer_times(district_name: str, school: int = 0) -> dict:
    url = "http://api.aladhan.com/v1/timingsByAddress"
    params = {
        "address": f"{district_name}, Uzbekistan",
        "method": 3, 
        "school": school
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    timings = data["data"]["timings"]
                    
                    # Barcha vaqtlarni tozalab olamiz
                    times = {
                        "Bomdod": timings["Fajr"],
                        "Quyosh": timings["Sunrise"],
                        "Peshin": timings["Dhuhr"],
                        "Asr": timings["Asr"],
                        "Shom": timings["Maghrib"],
                        "Xufton": timings["Isha"]
                    }
                    
                    # Jonli hisoblash uchun navbatdagi namozni aniqlash
                    next_prayer = get_next_prayer(times)
                    times["next_prayer"] = next_prayer
                    
                    return times
                return None
        except Exception as e:
            print(f"API xatosi: {e}")
            return None

def get_next_prayer(times: dict) -> str:
    """Hozirgi vaqtga qarab navbatdagi namozni aniqlaydi"""
    now = datetime.now().strftime("%H:%M")
    
    # Namoz vaqtlarini tartiblaymiz
    prayer_order = ["Bomdod", "Peshin", "Asr", "Shom", "Xufton"]
    
    for prayer in prayer_order:
        if times[prayer] > now:
            return f"{prayer} ({times[prayer]})"
            
    # Agar bugungi namozlar o'tib ketgan bo'lsa, ertangi bomdodni qaytaradi
    return f"Bomdod ({times['Bomdod']})"
