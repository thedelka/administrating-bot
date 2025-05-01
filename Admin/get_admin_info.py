import json
from Settings.get_config import get_config
def get_admins_ids_list():
    return [admin_info[0] for admin_info in json.loads(get_config("ADMIN", "admins"))]

