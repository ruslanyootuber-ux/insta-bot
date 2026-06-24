import os
import logging
from instagrapi import Client

logging.basicConfig(level=logging.INFO)

def run_bot():
    # Secret nomlari (Fly.io dagi kabi)
    session_id = os.getenv("SESSION_ID")
    
    if not session_id:
        print("Xatolik: SESSION_ID topilmadi!")
        return

    cl = Client()
    
    try:
        # ASOSIY QISM: Username/Password o'rniga session_id bilan kirish
        print("Sessiya orqali kirilmoqda...")
        cl.login_by_sessionid(session_id)
        print("Muvaffaqiyatli kirildi!")
        
        # Botingiz ishini davom ettiring
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    run_bot()
