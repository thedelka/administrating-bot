import json

from Entities.admin import Admin
from Settings.get_config import get_config
def get_admins_ids_list():
    return [admin_info[0] for admin_info in json.loads(get_config("ADMIN", "admins"))]


admins_list = [Admin(admin_info[0], admin_info[1]) for admin_info in json.loads(get_config("ADMIN", 'admins'))]

def get_admins_list():
    return admins_list