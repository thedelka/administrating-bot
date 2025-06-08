import os
import json
from sqlite3 import connect
from aiogram.types import Message
from bot_entities.user import User


def serialize_message(new_message : Message) -> dict:
    """Transforms message into dict with message information and returns it"""

    message_data = {
        'message_id' : new_message.message_id,
        'content_type' : new_message.content_type
    }

    if new_message.text:
        message_data['text'] = new_message.text
    elif new_message.caption:
        message_data['caption'] = new_message.caption

    if new_message.content_type != "text":
        media = getattr(new_message, new_message.content_type)
        message_data["file_id"] = media[-1].file_id if new_message.content_type == "photo" else media.file_id

    return message_data


class UserDatabaseManager:

    def __init__(self, db_name : str = "users_data.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = connect(self.db_path)
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
        """Add user if user_id is not already in database"""
        messages = [serialize_message(message) for message in user.user_message_history]
        json_data = json.dumps(messages)

        self.cursor.execute("SELECT user_id FROM users_data WHERE user_id = ?", (user.user_id,))
        user_id_value = self.cursor.fetchone()

        if user_id_value is None:
            self.cursor.execute("INSERT INTO users_data (user_id, user_name, user_messages) VALUES (?, ?, ?)",
                                (user.user_id, user.user_name, json_data))
            self.connection.commit()

    def get_user_messages(self, user_id):
        """Get user messages history as list of every message information (list of dicts)"""
        try:
            self.cursor.execute("SELECT user_messages FROM users_data WHERE user_id = ?",
                                (user_id,))
            user_messages_value = self.cursor.fetchone()

            if user_messages_value[0]:
                return [message for message in json.loads(user_messages_value[0])]
            return []
        except TypeError as e:
            print(f"[ERROR] Скорее всего, используется айди админа: {e}")

    def get_username(self, user_id):
        self.cursor.execute("SELECT user_name FROM users_data WHERE user_id = ?", (user_id, ))
        user_name = self.cursor.fetchone()[0]
        return user_name

    def add_message_to_user_message_history(self, user_id, new_message_data):
        try:
            messages = self.get_user_messages(user_id)
            messages.append(new_message_data)

            self.cursor.execute("UPDATE users_data SET user_messages = ? WHERE user_id = ?", (
                json.dumps(messages, ensure_ascii=False), user_id
            ))

            self.connection.commit()

        except json.JSONDecodeError as e:
            print(f"[ERROR] Произошла ошибка из-за некорректного JSON: {e}")
        except AttributeError as e:
            print(f"[ERROR]: {e}")

    def clear_user_message_history(self, user_id):
        self.cursor.execute("UPDATE users_data SET user_messages = NULL WHERE user_id = ?", (user_id,))
        self.connection.commit()


user_db_manager = UserDatabaseManager()