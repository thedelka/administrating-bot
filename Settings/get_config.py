"""Get config.txt info to use it anywhere"""
import configparser, os

def get_config(section_name, section_var):
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')

    config = configparser.ConfigParser()
    config.read(r'{}'.format(config_path), encoding='utf-8')

    return config.get(section_name, section_var)

