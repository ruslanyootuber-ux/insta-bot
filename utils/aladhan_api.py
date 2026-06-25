import aiohttp

async def get_prayer_times(district_name: str) -> dict:
    """
    Aladhan API orqali berilgan tuman uchun namoz vaqtlarini oladi.
    """
    # So'rov manzili (Address): Tuman, O'zbekiston
    address = f"{district_name}, Uzbekistan"
    url = "http://api.aladhan.com/v1/timingsByAddress"
    
    # Method 3: Muslim World League (Aksariyat O'zbekiston vaqtlariga yaqin)
    params = {
        "address": address,
        "method": 3
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
