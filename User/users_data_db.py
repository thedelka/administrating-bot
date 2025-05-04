import json
import pickle, sqlite3, os
from typing import Optional
from Entities.user import User

class UserDatabaseManager:

    def __init__(self, db_name : str = "users_data.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_data (
        user_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        user_messages TEXT
        )""")

        self.connection.commit()

    def add_user(self, user : User):
        messages = user.user_message_history
        json_data = json.dumps(messages, ensure_ascii=False)

        self.cursor.execute("SELECT user_id FROM users_data WHERE user_id = ?", (user.user_id,))
        user_id_value = self.cursor.fetchone()

        if user_id_value is None:
            self.cursor.execute("INSERT INTO users_data (user_id, user_name, user_messages) VALUES (?, ?, ?)",
                                (user.user_id, user.user_name, json_data))
            self.connection.commit()

    def get_user_attribute(self, user_id, attribute : str):
        self.cursor.execute(f"SELECT {attribute} FROM users_data WHERE user_id = ?",
                            (user_id,))
        user_attribute_value = self.cursor.fetchone()

        return user_attribute_value[0] if user_attribute_value is not None else None

    def update_user_message_history(self, user_id, new_message):
        self.cursor.execute("SELECT user_messages FROM users_data WHERE user_id = ?", (user_id,))
        user_data = self.cursor.fetchone()

        try:
            messages : list = json.loads(user_data[0] if user_data else [])

            if new_message:
                messages.append(new_message)
            else:
                messages = []

            self.cursor.execute("UPDATE users_data SET user_messages = ? WHERE user_id = ?", (
                json.dumps(messages, ensure_ascii=False), user_id
            ))
            self.connection.commit()
        except json.JSONDecodeError as e:
            print(f"Произошла ошибка из-за некорректного JSON: {e}")

db_manager = UserDatabaseManager()