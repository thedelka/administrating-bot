from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

user_message_builder = InlineKeyboardBuilder()

user_message_builder.add(InlineKeyboardButton(text="Ответить", callback_data="ANSWER"))
user_message_builder.add(InlineKeyboardButton(text="Просмотреть диалог", callback_data="DIALOGUE_CHECKOUT"))
user_message_builder.add(InlineKeyboardButton(text="Завершить диалог", callback_data="CLOSE_DIALOGUE"))

