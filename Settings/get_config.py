"""Get config.txt info to use it anywhere"""
import configparser, os, json
from BotEntities.admin import Admin

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
        self.config = configparser.ConfigParser()
        self.admins_list = self.get_admins_list()

    def get_config(self, section_name, section_var):
        self.config.read(r'{}'.format(self.config_path), encoding='utf-8')
        return json.loads(self.config.get(section_name, section_var))


    def get_admins_list(self) -> list[Admin]:
        """Usable only for reading, not writing"""
        admins_list = [Admin(admin_info[0], admin_info[1]) for admin_info in self.get_config("ADMIN", 'admins')]  # list of Admin-objects
        return admins_list

    def get_admins_ids_list(self) -> list:
        return [admin.admin_user_id for admin in self.admins_list]

    def get_admin(self, admin_id):
        for admin_info in self.admins_list:
            if admin_info.admin_user_id == admin_id:
                return admin_info

config_manager = ConfigManager()