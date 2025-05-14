import datetime
from pytz import timezone
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram import Router, Bot, F
from Settings.get_config import config_manager
from Database.users_data_db import  user_db_manager, serialize_message
from Database.admins_data_db import admin_db_manager
from States.dialogue_state import DialogueState
from Keyboards.user_message_keyboard import create_user_message_keyboard
from Handlers.commands_handler import send_message_according_to_type

router = Router()

async def send_type_message(message: Message,
                            bot : Bot,
                            target_admin_id):
    """Send user message to an admin"""
    tz = timezone(config_manager.get_config("BOT_CONSTANTS", "timezone"))
    time_now = datetime.datetime.now(tz).strftime("%H:%M:%S")

    user_id = message.from_user.id

    await bot.send_message(target_admin_id, f"❗ НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ {message.from_user.id} "
                                             f"\nДата отправки по UTC+3: {time_now}",
                           reply_markup=create_user_message_keyboard(message.from_user.id))

    if user_id not in admin_db_manager.admin_texting_user_id_operation(target_admin_id): admin_db_manager.admin_texting_user_id_operation(target_admin_id, user_id)

    await send_message_according_to_type(
                                        target_admin_id,
                                         bot,
                                         serialize_message(message),
                                         user_id
                                         )

    print(f"[DEBUG] Сообщения пользователя: "
          f"{user_db_manager.get_user_messages(user_id)}")
    print(f"[DEBUG_DB_SEND_TYPE_MESSAGE] "
          f"{admin_db_manager.get_db()}")


@router.message(StateFilter(None),
                F.from_user.id.not_in(config_manager.get_admins_ids_list()))
async def send_user_message(message : Message,
                            bot : Bot,
                            state : FSMContext):
    admin_with_lowest_queries_id = config_manager.get_free_admin(admin_db_manager.get_db())

    await send_type_message(message,
                            bot,
                            admin_with_lowest_queries_id)

    await message.answer(
            "Ваше сообщение успешно отправлено. Пожалуйста, подождите, пока мы найдем свободных операторов...")

    await state.set_state(DialogueState.dialogue_open)
    await state.set_data({"current_texting_admin_id" : admin_with_lowest_queries_id})

    print(f'[DEBUG] Текущее состояние диалога у юзера: {await state.get_state()}')


@router.message(StateFilter(DialogueState.dialogue_open),
                F.from_user.id.not_in(config_manager.get_admins_ids_list()))
async def message_while_dialogue(message : Message, bot : Bot, state: FSMContext):
    current_admin_id = dict(await state.get_data())["current_texting_admin_id"]
    await send_type_message(message, bot, current_admin_id)