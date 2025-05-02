import json

from Entities.admin import Admin
from Settings.get_config import get_config
def get_admins_ids_list():
    return [admin_info[0] for admin_info in json.loads(get_config("ADMIN", "admins"))]


admins_list = [Admin(admin_info[0], admin_info[1]) for admin_info in json.loads(get_config("ADMIN", 'admins'))]

def get_admin(admin_id):
    for admin_info in admins_list:
        if admin_info.admin_user_id == admin_id:
            return admin_info