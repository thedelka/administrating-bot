import json

from Keyboards.menu_keyboard import menu_buttons_texts
from Keyboards.menu_keyboard import menu_pages_builders
from Settings.get_config import get_config
from aiogram.types import CallbackQuery
from aiogram import Router, F
from Menu. menu_pages_changer import decrease_current_menu_page,increase_current_menu_page,get_current_menu_page

menu_buttons = json.loads(get_config("HELP_MENU_SETTINGS", "buttons"))
router = Router()


@router.callback_query(F.data.in_(menu_buttons_texts))
async def send_menu_button_text(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"{menu_buttons[callback.data]}")

@router.callback_query(F.data== ">>>")
async def increase_page(callback : CallbackQuery):
    increase_current_menu_page()

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=menu_pages_builders[get_current_menu_page()-1])

@router.callback_query(F.data == "<<<")
async def decrease_page(callback : CallbackQuery, ):
    decrease_current_menu_page()

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=menu_pages_builders[get_current_menu_page()-1])
