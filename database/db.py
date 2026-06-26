import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                district TEXT,
                reminder_time INTEGER DEFAULT 0,
                school INTEGER DEFAULT 0,
                rating INTEGER DEFAULT 0
            )
        """)
        # Agar oldindan jadval yaratilgan bo'lsa, xato bermasligi uchun try-except ishlatamiz
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN rating INTEGER DEFAULT 0")
        except:
            pass
        self.connection.commit()

    def add_user(self, user_id, full_name):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
        self.connection.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def update_district(self, user_id, district):
        self.cursor.execute("UPDATE users SET district = ? WHERE user_id = ?", (district, user_id))
        self.connection.commit()
    
    def update_reminder(self, user_id, time):
        self.cursor.execute("UPDATE users SET reminder_time = ? WHERE user_id = ?", (time, user_id))
        self.connection.commit()

    def update_school(self, user_id, school):
        self.cursor.execute("UPDATE users SET school = ? WHERE user_id = ?", (school, user_id))
        self.connection.commit()
        
    def get_user_data(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    # Yangi: Foydalanuvchi bahosini saqlash
    def update_rating(self, user_id, rating):
        self.cursor.execute("UPDATE users SET rating = ? WHERE user_id = ?", (rating, user_id))
        self.connection.commit()

    # Yangi: Umumiy reytingni hisoblash
    def get_rating_stats(self):
        self.cursor.execute("SELECT rating FROM users WHERE rating > 0")
        ratings = self.cursor.fetchall()
        
        if not ratings:
            return 0.0, 0  # O'rtacha baho, Odamlar soni
            
        total_voters = len(ratings)
        total_score = sum([r[0] for r in ratings])
        average = total_score / total_voters
        
        return round(average, 1), total_voters