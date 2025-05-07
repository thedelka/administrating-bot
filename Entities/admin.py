import json
from Settings.get_config import get_config

class Admin:
    def __init__(self, admin_user_id, admin_name=None, texting_user_id : list[int] = None):
        if texting_user_id is None:
            texting_user_id = []

        self.admin_user_id = admin_user_id
        self.admin_name = admin_name
        self.texting_user_id = texting_user_id
        self.admin_queries_count = len(self.texting_user_id)
        self.is_ready_for_work = False

admins_list = [Admin(admin_info[0], admin_info[1]) for admin_info in json.loads(get_config("ADMIN", 'admins'))] #list of Admin-objects

def get_admins_ids_list():
    return [admin_info[0] for admin_info in json.loads(get_config("ADMIN", "admins"))]


def get_admin(admin_id):
    for admin_info in admins_list:
        if admin_info.admin_user_id == admin_id:
            return admin_info