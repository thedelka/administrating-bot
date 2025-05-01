from aiogram.filters import Command
from aiogram.types import Message
from aiogram import  Router, Bot
from Jsons.jsons_creator import get_admins_ids_list
router = Router()

@router.message()
async def send_user_message(message : Message, bot : Bot):
    for admin_id in get_admins_ids_list():
        await bot.send_message(admin_id, message.text)