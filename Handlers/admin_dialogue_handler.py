import json
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from Entities.admin import get_admin, admins_list
from Settings.get_config import get_config
from aiogram.types import Message, CallbackQuery
from States.admin_state import AdminState
from aiogram import Router, Bot, F
from Keyboards.clean_message_history_keyboard import create_clean_history_keyboard
from Database.users_data_db import db_manager, serialize_message
from Handlers.commands_handler import send_message_according_to_type

router = Router()


@router.callback_query(F.data.startswith("ANSWER"))
async def start_messaging(callback : CallbackQuery, state : FSMContext, bot : Bot):
    await callback.answer("Ваша переписка с пользователем начата!")

    user_id = callback.data.split("_")[-1]

    operator_found_text = json.loads(get_config("MESSAGES", "found_not_taken_admin_text")) #сделать так чтобы это писалось только в первый раз нажатия

    await bot.send_message(user_id, operator_found_text)

    get_admin(callback.from_user.id).texting_user_id.append(user_id)

    await state.set_state(AdminState.texting)
    await state.set_data({"current_user_id" : user_id})

    print(f"Список обрабатывающихся админом пользователей: {get_admin(callback.from_user.id).texting_user_id}")


@router.message(StateFilter(AdminState.texting))
async def admin_answer_user(message : Message, bot : Bot, state : FSMContext):

    data = await state.get_data()
    current_user_id = data["current_user_id"]

    await send_message_according_to_type(current_user_id, bot, serialize_message(message))


@router.callback_query(F.data.startswith("DIALOGUE_CHECKOUT"))
async def get_dialogue_history(callback : CallbackQuery, state : FSMContext, bot : Bot):
    user_id = callback.data.split("_")[-1]
    await callback.answer()

    try:
        message_history = db_manager.get_user_messages(user_id)

        archive_messages = []
        archive_messes_text = await callback.message.answer("🗄Архивные сообщения🗄")
        archive_messages.append(archive_messes_text.message_id)

        for message in message_history:
            sent_message = await send_message_according_to_type(callback.message.chat.id, bot, message)
            archive_messages.append(sent_message.message_id)

        await callback.message.answer(f"⏫ИСТОРИЯ СООБЩЕНИЙ ПОЛЬЗОВАТЕЛЯ {user_id}", reply_markup=create_clean_history_keyboard(user_id).as_markup())
        await state.set_data({"temp_mess_history": archive_messages})

    except Exception as e:
        print(f"Во время отправления истории чата с пользователем произошла ошибка: {e}")

#TODO: логику рассылки обращений по свободным админам и кнопки админа "я готов" и "я устал" + сделать возможность админу отправлять фото с подписью
@router.callback_query(F.data.startswith("REMOVE_HISTORY"))
async def remove_dialogue_history(callback : CallbackQuery, state : FSMContext, bot : Bot):
    data = await state.get_data()
    archive_messages = data.get("temp_mess_history", [])
    admin_chat_id = callback.message.chat.id

    if archive_messages:
        try:
            await bot.delete_messages(admin_chat_id, archive_messages)
        except Exception as e:

            print(f"Ошибка при удалении сообщений: {e}")
            await callback.answer("❌ Не удалось удалить часть сообщений", show_alert=True)

    await callback.message.delete()

@router.callback_query(F.data.startswith("CLOSE_DIALOGUE"))
async def close_dialogue(callback : CallbackQuery , bot : Bot, state : FSMContext):
    user_id = callback.data.split("_")[-1]

    close_dialogue_text = json.loads(get_config("MESSAGES", "close_dialogue_text"))

    await bot.send_message(user_id, close_dialogue_text)
    db_manager.clear_user_message_history(user_id)

    if user_id in [admin.admin_user_id for admin in admins_list]:
        get_admin(callback.from_user.id).texting_user_id.remove(user_id)
    else:
        print("ТАКОГО ЮЗЕРА И ТАК НЕ БЫЛО!")

    await callback.message.answer(f"Чат с пользователем {user_id} завершён!")
    await state.clear()

    storage = state.storage
    target_key  = StorageKey(chat_id=int(user_id), user_id=int(user_id), bot_id = bot.id)
    await storage.set_state(key=target_key, state = None)

    print(f"Список обрабатывающихся админов пользователей: {get_admin(callback.from_user.id).texting_user_id}")
    print(f"Состояние пользователя: {await storage.get_state(key=target_key)}")