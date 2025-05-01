import pickle
import sqlite3
import os
from idlelib.colorizer import prog_group_name_to_tag

from Entities.dialogue import Dialogue
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
    except None:
        print("ТАКОЙ ПОЛЬЗОВАТЕЛЬ НЕ НАЙДЕН")
        return None

def add_dialogue(user_id, dialogue : Dialogue):
    cursor.execute("SELECT user FROM users_data WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    try:
        binary = user_data[0]
        user : User = pickle.loads(binary)

        dialogues = user.user_dialogues
        dialogues.append(dialogue)

        setattr(user, "user_dialogues", dialogues)

    except None:
        print("NO USER WITH THIS ID")

connection.commit()