from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, Bot
from Keyboards.menu_keyboard import menu_pages_builders
from Keyboards.admin_work_status_keyboard import get_work_status_kb
from Settings.get_config import config_manager
from Database.users_data_db import user_db_manager
from Database.admins_data_db import admin_db_manager
from BotEntities.user import User


router = Router()

@router.message(Command("start"))
async def start_command(message : Message):

    if message.from_user.id not in config_manager.get_admins_ids_list():

        start_text = config_manager.get_config("MESSAGES", 'start_text_user')
        help_user_text = config_manager.get_config("MESSAGES", 'help_user_text')

        user = User(message.from_user.id, message.from_user.username)
        user_db_manager.add_user(user)

        await message.answer(start_text, reply_markup=menu_pages_builders[0])
        await message.answer(help_user_text)

    else:
        start_text = config_manager.get_config("MESSAGES", "start_text_admin")
        await message.answer(start_text, reply_markup=get_work_status_kb(admin_db_manager.get_admin_is_ready(message.from_user.id)))

async def send_message_according_to_type(target_id,
                                         bot : Bot,
                                         message_data : dict,
                                         user_id =  None):
    """Check type of message and SEND MESSAGE ACCORDING TO its TYPE"""

    types_dict = {
        "text": lambda b, a_i: (b.send_message(a_i, message_data["text"])),
        "photo": lambda b, a_i: (b.send_photo(a_i, message_data["file_id"], caption=message_data.get("caption"))),
        "document": lambda b, a_i: (b.send_document(a_i, message_data["file_id"], caption=message_data.get("caption"))),
        "sticker": lambda b, a_i: (b.send_sticker(a_i, message_data["file_id"])),
        "video": lambda b, a_i: (b.send_video(a_i, message_data["file_id"], caption=message_data.get("caption"))),
        "voice": lambda b, a_i: (b.send_voice(a_i, message_data["file_id"]))
    }

    for attribute, send_method in types_dict.items():

        if message_data["content_type"] == attribute:

            if user_id:
                user_db_manager.add_message_to_user_message_history(user_id, message_data)

            return await send_method(bot, target_id)