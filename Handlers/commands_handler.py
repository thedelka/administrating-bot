from Keyboards.menu_keyboard import menu_pages_builders
import json
from Settings.get_config import get_config
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import  Router
from User.users_data_db import add_user
from User.user import User

router = Router()


@router.message(Command("start"))
async def start_command(message : Message):

    start_text = json.loads(get_config("START_MESSAGE", 'start_text'))

    user = User(message.from_user.id, message.from_user.username)
    add_user(user)

    await message.answer(text=start_text, reply_markup=menu_pages_builders[0])


#TODO: в зависимости какя щас страница, выводим тот билдер из списка которй равен page-1 по индексу