import pickle
import sqlite3
import os
from Entities.user import User

db_path = os.path.join(os.path.dirname(__file__), "users_data.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users_data (
user_id INTEGER NOT NULL,
user BLOB
)""")

connection.commit()

def add_user(user : User):
    cursor.execute("SELECT user_id FROM users_data WHERE user_id = ?", (user.user_id,))
    user_id_value = cursor.fetchone()

    if user_id_value is None:
        cursor.execute("INSERT INTO users_data (user_id, user) VALUES (?, ?)", (user.user_id, pickle.dumps(user)))
        connection.commit()


def get_user(user_id):
    cursor.execute("SELECT user FROM users_data WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    try:
        binary_data = user_data[0]
        user = pickle.loads(binary_data)

        return user

    except None as e:
        print(e)
        return None

def add_message_to_history(user_id, new_message):
    cursor.execute("SELECT user FROM users_data WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    try:
        binary = user_data[0]
        user : User = pickle.loads(binary)

        user.user_message_history.append(new_message)

        setattr(user, "user_message_history", user.user_message_history)

        cursor.execute("UPDATE users_data set user = ? WHERE user_id = ?", (pickle.dumps(user), user_id))
        connection.commit()

    except (TypeError, IndexError) as e:
        print(f"Ошибка при обновлении истории сообщений пользователя: {e}")

    except Exception as e:
        print(f"Произошла другая ошибка: {e}")

connection.commit()