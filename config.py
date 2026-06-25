import os
from dotenv import load_dotenv

# .env faylini o'qish
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("XATOLIK: .env faylida BOT_TOKEN topilmadi!")