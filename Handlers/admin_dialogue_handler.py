from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot, F

from Settings.get_config import config_manager

import logging

from States.admin_state import AdminState

from Keyboards.clean_message_history_keyboard import create_clean_history_keyboard

from Database.users_data_db import user_db_manager, serialize_message
from Database.admins_data_db import admin_db_manager

from Handlers.commands_handler import send_message_according_to_type

logger = logging.getLogger(__name__)
router = Router()

async def remove_user_id(user_id,
                         admin_id,
                         callback : CallbackQuery,
                         state : FSMContext,
                         bot : Bot):
    user_id = int(user_id)

    if user_id in admin_db_manager.admin_texting_user_id_operation(admin_id):
        admin_db_manager.admin_texting_user_id_operation(admin_id, user_id, True)

        await callback.message.answer(f"Чат с пользователем {user_id} завершён!")
        await state.clear()

        storage = state.storage
        target_key = StorageKey(chat_id=user_id, user_id=user_id, bot_id=bot.id)
        await storage.set_state(key=target_key, state=None)

        print("[DEBUG] Состояние пользователя:"
              f" {await storage.get_state(key=target_key)}")

    else:
        print("[DEBUG] Такого юзера и так не было,"
              " нечего удалять из списка.")

    print(f"[DEBUG_DB_REMOVE_USER_ID] {admin_db_manager.get_db()}")

@router.callback_query(F.data.startswith("ANSWER"))
async def start_messaging(callback : CallbackQuery,
                          state : FSMContext,
                          bot : Bot):
    await callback.answer("Ваша переписка с пользователем начата!")
    user_id = callback.data.split("_")[-1]
    operator_found_text = config_manager.get_config("MESSAGES", "found_not_taken_admin_text")

    await bot.send_message(user_id, operator_found_text)

    await state.set_state(AdminState.texting)
    await state.set_data({"current_user_id" : user_id})
    print(f"[DEBUG_DB_ANSWER] {admin_db_manager.get_db()}")


@router.message(StateFilter(AdminState.texting),
                ~F.text.in_(["Готов к работе", "Взять паузу"]))
async def admin_answer_user(message : Message,
                            bot : Bot,
                            state : FSMContext):

    data = await state.get_data()
    current_user_id = data["current_user_id"]

    await send_message_according_to_type(
        current_user_id, bot, serialize_message(message)
    )


@router.callback_query(F.data.startswith("DIALOGUE_CHECKOUT"))
async def get_dialogue_history(callback : CallbackQuery,
                               state : FSMContext,
                               bot : Bot):
    user_id = int(callback.data.split("_")[-1])
    await callback.answer()

    message_history = user_db_manager.get_user_messages(user_id)

    archive_messages = []
    archive_messages_text = await callback.message.answer("⏬Архивные сообщения⏬")
    archive_messages.append(archive_messages_text.message_id)

    for message in message_history:
        sent_message = await send_message_according_to_type(
            callback.message.chat.id,
            bot,
            message)

        archive_messages.append(sent_message.message_id)

    await callback.message.answer(f"⏫ИСТОРИЯ СООБЩЕНИЙ ПОЛЬЗОВАТЕЛЯ {user_id}⏫",
                                  reply_markup=create_clean_history_keyboard(user_id).as_markup())
    await state.set_data({"temp_mess_history": archive_messages})

@router.callback_query(F.data.startswith("REMOVE_HISTORY"))
async def remove_dialogue_history(callback : CallbackQuery,
                                  state : FSMContext,
                                  bot : Bot):
    data = await state.get_data()
    archive_messages = data.get("temp_mess_history", [])
    admin_chat_id = callback.message.chat.id

    if archive_messages:
        try:
            await bot.delete_messages(admin_chat_id, archive_messages)
        except Exception as e:
            print(f"[ERROR] Ошибка при удалении сообщений: {e}")

    await callback.message.delete()

@router.callback_query(F.data.startswith("CLOSE_DIALOGUE"))
async def close_dialogue(callback : CallbackQuery ,
                         bot : Bot,
                         state : FSMContext):

    user_id = callback.data.split("_")[-1]
    admin_id = callback.from_user.id

    close_dialogue_text = config_manager.get_config(
        "MESSAGES",
        "close_dialogue_text"
    )

    await bot.send_message(user_id, close_dialogue_text)
    user_db_manager.clear_user_message_history(user_id)

    await remove_user_id(user_id, admin_id, callback, state, bot)