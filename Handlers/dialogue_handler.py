import datetime
import pytz
from User.users_data_db import  get_user, add_message_to_history
from aiogram.types import Message
from aiogram import  Router, Bot
from Admin.get_admin_info import get_admins_ids_list

router = Router()

@router.message()
async def send_user_message(message : Message, bot : Bot):
    """Send user message to an admin with details"""

    user_id = message.from_user.id

    tz_moscow = pytz.timezone('Europe/Moscow')
    time_now = datetime.datetime.now(tz_moscow).strftime("%H:%M:%S")

    for admin_id in get_admins_ids_list():

        await bot.send_message(admin_id, f"❗ НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ "
                                         f"\n\nID пользователя: {message.from_user.id}\nИмя пользователя: @{message.from_user.username}\n"
                                         f"Дата отправки по UTC+3: {time_now}")
        await message.answer("Ваше сообщение успешно отправлено. Пожалуйста, подождите, пока мы найдем свободных операторов...")

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