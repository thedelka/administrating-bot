import json
import sqlite3, os
from Entities.admin import Admin

class AdminDatabaseManager:
    def __init__(self, db_name : str = "admins_data.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()


    def _create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins_data(
                            admin_id INTEGER NOT NULL,
                            admin_name TEXT NOT NULL,
                            admin_texting_user_id TEXT,
                            admin_states_info TEXT""")

        self.connection.commit()

    def add_admin(self, admin: Admin):
        admins_texting_user_id = admin.texting_user_id
        json_texting_users_data = json.dumps(admins_texting_user_id)

        self.cursor.execute("SELECT admin_id FROM admins_data WHERE admin_id = ?", (admin.admin_user_id,))
        admin_id_value = self.cursor.fetchone()

        if admin_id_value is None:
            self.cursor.execute("INSERT INTO admins_data (admin_id, admin_name, admin_texting_user_id, admin_states_info) VALUES (?, ?, ?, ?)",
                                (admin.admin_user_id, admin.admin_name, json_texting_users_data))
            self.connection.commit()