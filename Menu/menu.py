from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class Menu:
    def __init__(self, menu_buttons : dict):
        self.menu_buttons = menu_buttons


    def build_menu_keyboard(self):
        builder = InlineKeyboardBuilder()

        for button_text, button_callback_data in self.menu_buttons.items():
            builder.add(InlineKeyboardButton(text=button_text, callback_data=button_callback_data))

        builder.row(InlineKeyboardButton(text="<<<", callback_data="<<<"),
                            InlineKeyboardButton(text=">>>", callback_data=">>>"))
        return builder.as_markup()



