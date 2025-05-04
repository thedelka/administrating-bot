import datetime, json
from aiogram.fsm.context import FSMContext
from pytz import timezone
from Settings.get_config import get_config
from User.users_data_db import  db_manager
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram import Router, Bot
from Entities.admin import get_admins_ids_list
from States.dialogue_state import DialogueState
from Keyboards.user_message_keyboard import create_user_message_keyboard

router = Router()

async def send_message_according_to_type(admin_id, bot : Bot, message : Message, user_id):
    types_dict = {
        "text": (lambda b, a_i :  b.send_message(a_i, message.text)),
        "photo": (lambda b, a_i : b.send_photo(a_i, message.photo[-1].file_id)),
        "document": (lambda b, a_i : b.send_document(a_i, message.document.file_id)),
        "sticker": (lambda b, a_i : b.send_sticker(a_i, message.sticker.file_id)),
        "video": (lambda b, a_i : b.send_video(a_i, message.video.file_id)),
        "voice": (lambda b, a_i : b.send_voice(a_i, message.voice.file_id))
    }

    for attribute, send_method in types_dict.items():
        if getattr(message, attribute, None):
            await send_method(bot, admin_id)
            db_manager.update_user_message_history(user_id, getattr(message, attribute))


async def send_type_message(message: Message, bot : Bot):
    """Send user message to an admin"""

    tz = timezone(json.loads(get_config("BOT_CONSTANTS", "timezone")))

    time_now = datetime.datetime.now(tz).strftime("%H:%M:%S")

    user_id = message.from_user.id

    for admin_id in get_admins_ids_list():
        await bot.send_message(admin_id, f"❗ НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ "
                                         f"\n\nID пользователя: {message.from_user.id}\nИмя пользователя: @{message.from_user.username}\n"
                                         f"Дата отправки по UTC+3: {time_now}", reply_markup=create_user_message_keyboard(message.from_user.id))

        await send_message_according_to_type(admin_id, bot, message, user_id)

    print(db_manager.get_user_attribute(user_id, "user_messages"))


@router.message(StateFilter(None))
async def send_user_message(message : Message, bot : Bot, state : FSMContext):

    await send_type_message(message, bot)

    await message.answer(
        "Ваше сообщение успешно отправлено. Пожалуйста, подождите, пока мы найдем свободных операторов...")

    await state.set_state(DialogueState.dialogue_open)

    print(f'Текуще состояние диалога у юзера: {await state.get_state()}')


@router.message(StateFilter(DialogueState.dialogue_open))
async def message_while_dialogue(message : Message, bot : Bot):
    await send_type_message(message, bot)