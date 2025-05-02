from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def create_clean_history_keyboard(user_id):
    remove_history_builder = InlineKeyboardBuilder()

    remove_history_builder.add(InlineKeyboardButton(text="Скрыть историю", callback_data=f"REMOVE_HISTORY_{user_id}"))

    return remove_history_builder