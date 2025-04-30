import configparser
import json
from Settings.get_config import get_config

menu_buttons_texts = json.loads(get_config("HELP_MENU_SETTINGS", "buttons"))
print(menu_buttons_texts.keys())