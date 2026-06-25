import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Foydalanuvchilar jadvali
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                district TEXT
            )
        """)
        self.connection.commit()

    def add_user(self, user_id, full_name):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
        self.connection.commit()

    def update_district(self, user_id, district):
        self.cursor.execute("UPDATE users SET district = ? WHERE user_id = ?", (district, user_id))
        self.connection.commit()

    def get_user_district(self, user_id):
        self.cursor.execute("SELECT district FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None