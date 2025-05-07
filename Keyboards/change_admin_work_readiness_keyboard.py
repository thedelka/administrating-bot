from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_work_readiness_keyboard(admin_is_ready_for_work : bool):
    kb = [
        [KeyboardButton(text="Готов к работе" if not admin_is_ready_for_work else "Взять паузу")]
    ]

    result_keyboard = ReplyKeyboardMarkup(keyboard= kb, resize_keyboard=True)
    return result_keyboard