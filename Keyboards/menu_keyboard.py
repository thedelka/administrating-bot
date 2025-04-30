import json
from Menu.menu import Menu
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from Settings.get_config import get_config

menu_buttons_texts = list(json.loads(get_config("HELP_MENU_SETTINGS", "buttons")).keys())

buttons_quantity = len(menu_buttons_texts)
buttons_for_page = json.loads(get_config("HELP_MENU_SETTINGS", "buttons_for_page"))
max_menu_pages = buttons_quantity // buttons_for_page
last_page_buttons_count = buttons_quantity % buttons_for_page

menu_pages_builders = []


button_index = 0
for _ in range(max_menu_pages):

    page_buttons = {}

    for _ in range(buttons_for_page):

        current_button = menu_buttons_texts[button_index].replace("\u200d", "") #\u200d пишется перед смайлами, его надо убрать

        button_index += 1 if button_index < buttons_quantity else button_index
        page_buttons[current_button] = current_button

    menu_pages_builders.append(Menu(page_buttons).build_menu_keyboard())

if last_page_buttons_count > 0:

    last_buttons = menu_buttons_texts[-last_page_buttons_count:]

    last_page_buttons_dict = {}

    for button in last_buttons:
        last_page_buttons_dict[button] = button

    menu_pages_builders.append(Menu(last_page_buttons_dict).build_menu_keyboard())