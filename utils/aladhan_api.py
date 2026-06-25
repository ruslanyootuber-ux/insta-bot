import aiohttp

async def get_prayer_times(district_name: str, school: int = 0) -> dict:
    """
    Aladhan API orqali berilgan tuman va mazhab uchun namoz vaqtlarini oladi.
    school: 0 = Hanafi, 1 = Shafi'i
    """
    url = "http://api.aladhan.com/v1/timingsByAddress"
    
    params = {
        "address": f"{district_name}, Uzbekistan",
        "method": 3,   # Muslim World League
        "school": school # Mazhabni uzatamiz
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    timings = data["data"]["timings"]
                    
                    return {
                        "Bomdod": timings["Fajr"],
                        "Quyosh": timings["Sunrise"],
                        "Peshin": timings["Dhuhr"],
                        "Asr": timings["Asr"],
                        "Shom": timings["Maghrib"],
                        "Xufton": timings["Isha"]
                    }
                else:
                    return None
        except Exception as e:
            print(f"API xatosi: {e}")
            return None