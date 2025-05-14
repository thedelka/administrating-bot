from Keyboards.menu_keyboard import menu_buttons_texts
from Keyboards.menu_keyboard import menu_pages_builders

from Settings.get_config import config_manager

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router, F

from Menu. menu_pages_changer import (decrease_current_menu_page,
                                      increase_current_menu_page,
                                      get_current_menu_page)

menu_buttons = config_manager.get_config("HELP_MENU_SETTINGS", "buttons")
router = Router()


@router.callback_query(F.data.in_(menu_buttons_texts))
async def send_menu_button_text(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"{menu_buttons[callback.data]}")

@router.callback_query(F.data== ">>>")
async def increase_page(callback : CallbackQuery, state: FSMContext):
    increase_current_menu_page()

    await state.set_data({"current_menu_page" : get_current_menu_page()})
    current_menu_page = dict(await state.get_data())["current_menu_page"]

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=menu_pages_builders[current_menu_page-1])

@router.callback_query(F.data == "<<<")
async def decrease_page(callback : CallbackQuery, state: FSMContext):
    decrease_current_menu_page()

    await state.set_data({"current_menu_page" : get_current_menu_page()})
    current_menu_page = dict(await state.get_data())["current_menu_page"]

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=menu_pages_builders[current_menu_page-1])
