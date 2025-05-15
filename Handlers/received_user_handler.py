from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from Database.users_data_db import user_db_manager
from Keyboards.received_user_keyboard import get_user_operation_kb
from Handlers.commands_handler import send_message_according_to_type


router = Router()

@router.callback_query(F.data.startswith("HISTORY_"))
async def show_user_history(callback : CallbackQuery, bot : Bot):
    user_id = callback.data.split("_")[-1]
    user_messages = user_db_manager.get_user_messages(user_id)

    for message_data in user_messages:
        await send_message_according_to_type(callback.from_user.id,
                                             bot, message_data)
    await callback.message.answer("Нажмите кнопку, чтобы начать диалог с пользователем", reply_markup=get_user_operation_kb(user_id))