import json, sqlite3, os
from BotEntities.admin import Admin
from Settings.get_config import config_manager

def _fill_admin_db(admins_list=config_manager.get_admins_list()):
    current_admin_ids = {admin.admin_user_id for admin in admins_list}

    admin_db_manager.cursor.execute("SELECT admin_id FROM admins_data")
    db_admin_ids = {row[0] for row in admin_db_manager.cursor.fetchall()}

    for admin_info in admins_list:
        admin_db_manager.add_admin(admin_info)

    for db_admin_id in db_admin_ids - current_admin_ids:
        admin_db_manager.remove_admin(db_admin_id)


class AdminDatabaseManager:

    def __init__(self, db_name : str = "admins_data.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins_data(
                            admin_id INTEGER NOT NULL,
                            admin_name TEXT NOT NULL,
                            admin_texting_user_id TEXT,
                            admin_queries_count INTEGER NOT NULL,
                            admin_is_ready BOOLEAN)""")

        self.connection.commit()

    def add_admin(self, admin: Admin):
        admin_texting_user_id = admin.texting_user_id
        json_texting_users_data = json.dumps(admin_texting_user_id)

        self.cursor.execute("SELECT admin_id FROM admins_data WHERE admin_id = ?", (admin.admin_user_id,))
        admin_id_value = self.cursor.fetchone()

        if admin_id_value is None:
            self.cursor.execute("INSERT INTO admins_data (admin_id, admin_name, admin_texting_user_id, admin_queries_count, admin_is_ready) VALUES (?, ?, ?, ?, ?)",
                                (admin.admin_user_id, admin.admin_name, json_texting_users_data, admin.admin_queries_count, admin.is_ready))
            self.connection.commit()

    def remove_admin(self, admin_id):
        self.cursor.execute("DELETE FROM admins_data WHERE admin_id = ?", (admin_id,))
        self.connection.commit()

    def get_db(self):
        self.cursor.execute("SELECT * FROM admins_data")
        data = self.cursor.fetchall()

        return data

    def clear_admin_texting_user_id(self, admin_id):
        self.cursor.execute("UPDATE admins_data SET admin_texting_user_id = NULL WHERE admin_id = ?", (admin_id,))
        self.connection.commit()

    def admin_texting_user_id_operation(self, admin_id, user_id= None, remove = False):
        """Returns admin_texting_user_id if user_id = None, updates admin_texting_user_id if user_id not None, removes
        user_id form texting_user_id if remove = True and user_id not None"""

        self.cursor.execute("SELECT admin_texting_user_id FROM admins_data WHERE admin_id = ?", (admin_id,))
        row = self.cursor.fetchone()

        if row and row[0]:
            json_data : list = json.loads(row[0])
        else:
            json_data = []

        try:
            if user_id:
                json_data.remove(user_id) if remove else json_data.append(user_id)
                self.cursor.execute("UPDATE admins_data SET admin_texting_user_id = ?, admin_queries_count = ? WHERE admin_id = ?",
                                        (json.dumps(json_data, ensure_ascii=False), len(json_data), admin_id))
                self.connection.commit()

                return None
        except ValueError:
            print("[ERROR] Такого пользователя и так не было.")

        return json_data

    def change_admin_is_ready(self, admin_id):
        """Changes admin_is_ready to opposite value"""
        self.cursor.execute("SELECT admin_is_ready FROM admins_data WHERE admin_id = ?", (admin_id,))
        data = self.cursor.fetchone()

        current_is_ready = data[0]
        current_is_ready = not current_is_ready

        self.cursor.execute("UPDATE admins_data SET admin_is_ready = ? WHERE admin_id = ?", (current_is_ready, admin_id))
        self.connection.commit()

    def get_admin_is_ready(self, admin_id):
        self.cursor.execute("SELECT admin_is_ready FROM admins_data WHERE admin_id = ?", (admin_id,))

        current_is_ready = self.cursor.fetchone()[0]
        return current_is_ready

admin_db_manager = AdminDatabaseManager()
_fill_admin_db()