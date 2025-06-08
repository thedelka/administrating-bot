from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

em_shut_kb_builder = InlineKeyboardBuilder()
em_shut_kb_builder.add(InlineKeyboardButton(text="✅Подтвердить", callback_data="CONFIRM_EM_SHUTDOWN"),
                       InlineKeyboardButton(text="❌Отменить", callback_data="CANCEL_EM_SHUTDOWN"))
