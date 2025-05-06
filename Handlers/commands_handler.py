import json
from Keyboards.menu_keyboard import menu_pages_builders
from Settings.get_config import get_config
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, Bot
from Database.users_data_db import db_manager
from Entities.user import User
from Database.users_data_db import serialize_message

router = Router()


@router.message(Command("start"))
async def start_command(message : Message):

    start_text = json.loads(get_config("MESSAGES", 'start_text'))
    help_user_text = json.loads(get_config("MESSAGES", 'help_user_text'))

    user = User(message.from_user.id, message.from_user.username)
    db_manager.add_user(user)

    await message.answer(text=start_text, reply_markup=menu_pages_builders[0])

    await message.answer(f"{help_user_text}")

async def send_message_according_to_type(target_id, bot : Bot, message_data : dict, user_id =  None):
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
                db_manager.add_message_to_user_message_history(user_id, message_data)

            return await send_method(bot, target_id)