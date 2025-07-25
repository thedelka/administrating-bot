"""
Get config.txt info to use it anywhere
Get admins"""
from typing import Optional
import configparser
import os
import json
from bot_entities.admin import Admin


class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
        self.config = configparser.ConfigParser()
        self.admins_list = self.get_admins_list()

    def get_config(self, section_name, section_var):
        self.config.read(r'{}'.format(self.config_path), encoding='utf-8')
        return json.loads(self.config.get(section_name, section_var))


    def get_admins_list(self) -> list[Admin]:
        """Returns Admin-objects list for reading"""
        admins_list = [Admin(admin_info[0], admin_info[1]) for admin_info in self.get_config("ADMIN", 'admins')]
        return admins_list

    def get_admins_ids_list(self) -> list:
        return [admin.admin_user_id for admin in self.admins_list]

    def get_admin(self, admin_id):
        for admin_info in self.admins_list:
            if admin_info.admin_user_id == admin_id:
                return admin_info

    def get_free_admin(self, admins: list[tuple]) -> Optional[int]:
        available_admins = [admin for admin in admins if admin[4]]

        if not available_admins:
            return None

        min_queries = min(admin[3] for admin in available_admins)

        min_queries_admins = [admin for admin in available_admins if admin[3] == min_queries]

        return min_queries_admins[0][0]

config_manager = ConfigManager()