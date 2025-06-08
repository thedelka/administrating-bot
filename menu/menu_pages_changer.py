from keyboards.menu_keyboard import menu_pages_builders


max_menu_pages = len(menu_pages_builders)
current_menu_page = 1

def get_current_menu_page():
    return current_menu_page

def increase_current_menu_page():
    global current_menu_page

    if current_menu_page < max_menu_pages:
        current_menu_page += 1

    elif current_menu_page == max_menu_pages:
        current_menu_page = 1


def decrease_current_menu_page():
    global current_menu_page

    if current_menu_page > 1:
        current_menu_page -= 1

    elif current_menu_page == 1:
        current_menu_page = max_menu_pages

