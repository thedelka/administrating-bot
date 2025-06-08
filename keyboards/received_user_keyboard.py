from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def get_show_messages_kb(user_id):
    user_mess_history_builder = InlineKeyboardBuilder()

    user_mess_history_builder.add(InlineKeyboardButton(text="Просмотреть сообщения", callback_data=f"HISTORY_{user_id}"))

    return user_mess_history_builder.as_markup()

def get_user_operation_kb(user_id):
    user_opers_builder = InlineKeyboardBuilder()
    user_opers_builder.add(InlineKeyboardButton(text="Начать диалог", callback_data=f"ANSWER_{user_id}"))
    return user_opers_builder.as_markup()