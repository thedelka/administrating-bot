import datetime
import json

from aiogram.fsm.context import FSMContext
from pytz import timezone
from Settings.get_config import get_config
from User.users_data_db import  get_user, add_message_to_history
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram import  Router, Bot
from Admin.get_admin_info import get_admins_ids_list
from States.dialogue_state import DialogueState
from Keyboards.user_message_keyboard import user_message_builder
router = Router()

async def send_type_message(message: Message, bot : Bot, admin_id):
    """Send user message to an admin"""

    user_id = message.from_user.id

    if message.text:
        await bot.send_message(admin_id, message.text)
        add_message_to_history(user_id, message.text)

    if message.photo:
        await bot.send_photo(admin_id, message.photo[-1].file_id)
        add_message_to_history(user_id, message.photo[-1].file_id)

    if message.document:
        await bot.send_document(admin_id, message.document.file_id)
        add_message_to_history(user_id, message.document.file_id)

    if message.sticker:
        await bot.send_sticker(admin_id, message.sticker.file_id)
        add_message_to_history(user_id, message.sticker.file_id)

    if message.voice:
        await bot.send_voice(admin_id, message.voice.file_id)
        add_message_to_history(user_id, message.voice.file_id)

    if message.video:
        await bot.send_video(admin_id, message.video.file_id)
        add_message_to_history(user_id, message.video.file_id)

    print(get_user(user_id).user_message_history)


@router.message(StateFilter(None))
async def send_user_message(message : Message, bot : Bot, state : FSMContext):

    tz = timezone(json.loads(get_config("BOT_CONSTANTS", "timezone")))
    time_now = datetime.datetime.now(tz).strftime("%H:%M:%S")

    for admin_id in get_admins_ids_list():
        await bot.send_message(admin_id, f"❗ НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ "
                                         f"\n\nID пользователя: {message.from_user.id}\nИмя пользователя: @{message.from_user.username}\n"
                                         f"Дата отправки по UTC+3: {time_now}", reply_markup=user_message_builder.as_markup())

        await message.answer(
            "Ваше сообщение успешно отправлено. Пожалуйста, подождите, пока мы найдем свободных операторов...")

        await send_type_message(message, bot, admin_id)

    await state.set_state(DialogueState.dialogue_open)

@router.message(StateFilter(DialogueState.dialogue_open))
async def while_dialogue(message: Message, bot: Bot, state : FSMContext): #работает
    pass #TODO: реализовать что пока диалог открыт пользователю не отвечают чт его сообщение успешно отправлено. и так далее по плану, все кнопки и тд