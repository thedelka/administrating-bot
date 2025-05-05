import json
from aiogram.fsm.context import FSMContext
from Keyboards.menu_keyboard import menu_pages_builders
from Settings.get_config import get_config
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import  Router
from User.users_data_db import db_manager
from Entities.user import User

router = Router()


@router.message(Command("start"))
async def start_command(message : Message):

    start_text = json.loads(get_config("MESSAGES", 'start_text'))
    help_user_text = json.loads(get_config("MESSAGES", 'help_user_text'))

    user = User(message.from_user.id, message.from_user.username)
    db_manager.add_user(user)

    await message.answer(text=start_text, reply_markup=menu_pages_builders[0])

    await message.answer(f"{help_user_text}")