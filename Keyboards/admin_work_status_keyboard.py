from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

_kb_admin_ready = [
        [KeyboardButton(text="Готов к работе")]
    ]
_kb_admin_not_ready =[
        [KeyboardButton(text="Взять паузу")]
    ]

result_keyboard_ready = ReplyKeyboardMarkup(keyboard= _kb_admin_ready, resize_keyboard=True)
result_keyboard_not_ready = ReplyKeyboardMarkup(keyboard= _kb_admin_not_ready, resize_keyboard=True)

def get_work_status_kb(admin_work_status):
    return result_keyboard_not_ready if admin_work_status else result_keyboard_ready
