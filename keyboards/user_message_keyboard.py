from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def create_user_message_keyboard(user_id):
    user_message_builder = InlineKeyboardBuilder()

    user_message_builder.add(InlineKeyboardButton(text="Ответить", callback_data=f"ANSWER_{user_id}"))
    user_message_builder.add(InlineKeyboardButton(text="Просмотреть диалог", callback_data=f"DIALOGUE_CHECKOUT_{user_id}"))
    user_message_builder.add(InlineKeyboardButton(text="Завершить диалог", callback_data=f"CLOSE_DIALOGUE_{user_id}"))

    return user_message_builder.as_markup()