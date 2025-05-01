"""
создание json-файлов, занесение туда данных и создание переменных, в которых хранятся данные из разных json-файлов соответственно
"""
import json
import os

admins_json_path = os.path.join(os.path.dirname(__file__), "admins.json")

def get_admins_ids_list():
    with open (admins_json_path, 'r') as file:
        data = json.load(file)

    return [data[i]['admin_user_id'] for i in data.keys()]

