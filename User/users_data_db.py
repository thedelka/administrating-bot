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
        user BLOB
        )""")

        self.connection.commit()

    def add_user(self, user : User):
        self.cursor.execute("SELECT user_id FROM users_data WHERE user_id = ?", (user.user_id,))
        user_id_value = self.cursor.fetchone()

        if user_id_value is None:
            self.cursor.execute("INSERT INTO users_data (user_id, user) VALUES (?, ?)", (user.user_id, pickle.dumps(user)))
            self.connection.commit()

    def get_user(self, user_id : int) -> Optional[User]:
        self.cursor.execute("SELECT user FROM users_data WHERE user_id = ?", (user_id,))
        user_data = self.cursor.fetchone()

        try:
            binary_data = user_data[0]
            user = pickle.loads(binary_data)

            return user

        except Exception as e:
            print(f"Произошла ошибка! {e}")
            return None

    def update_user_message_history(self, user_id, new_message):
        self.cursor.execute("SELECT user FROM users_data WHERE user_id = ?", (user_id,))
        user_data = self.cursor.fetchone()

        try:
            user : User = pickle.loads(user_data[0])

            if new_message is not None:
                user.user_message_history.append(new_message)
            else:
                user.user_message_history = []  # Resets history if None

            setattr(user, "user_message_history", user.user_message_history)

            self.cursor.execute("UPDATE users_data SET user = ? WHERE user_id = ?", (pickle.dumps(user), user_id))
            self.connection.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

db_manager = UserDatabaseManager()