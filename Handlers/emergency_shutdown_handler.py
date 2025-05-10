from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, Bot

from Keyboards.emergency_shudown_keyboard import em_shut_kb_builder

from Settings.get_config import config_manager

from Database.admins_data_db import admin_db_manager
from Database.users_data_db import user_db_manager

from asyncio import sleep

router = Router()

@router.message(Command("em_shutdown"), F.from_user.id.in_(config_manager.get_admins_ids_list()))
async def start_admin_emergency_shutdown(message : Message):
    await message.answer("❗Вы нажали кнопку экстренного отключения❗\n\n Все ваши обращения пользователей будут переведены на другого оператора❗",
                         reply_markup=em_shut_kb_builder.as_markup())

@router.callback_query(F.data == "CONFIRM_EM_SHUTDOWN")
async def confirm_shutdown(callback : CallbackQuery, bot : Bot):
    admin_id = callback.from_user.id

    await callback.message.answer("✅Экстренное перенаправление пользователей подтверждено. Все ваши пользователи:\n\n"
                                  f"{admin_db_manager.admin_texting_user_id_operation(callback.message.from_user.id)}\n\nбыли переведены на свободного оператора.")
    await callback.message.delete()

    free_admin_id = config_manager.get_free_admin(admin_db_manager.get_db())
    print(f"[DEBUG] Айди свободного админа : {free_admin_id}")
    user_ids_to_remove = admin_db_manager.admin_texting_user_id_operation(admin_id) #получение айди юзеров админа, нажавшего на кнопку
    admin_db_manager.clear_admin_texting_user_id(admin_id) #удаляем всех юзеров у админа нажавшего на кнопку

    await bot.send_message(chat_id=free_admin_id, text=f"❗Оператор {admin_id} нажал кнопку экстренного перенаправления пользователей и передал вам свои пользовательские обращения.\n\n"
                                          "Список переданных вам пользователей:")

    for user_id in user_ids_to_remove: #добавляем всех юзеров свободному админу
        admin_db_manager.admin_texting_user_id_operation(free_admin_id, user_id)
        await bot.send_message(chat_id=free_admin_id, text=f"{user_id} - {user_db_manager.get_username(user_id)}")

@router.callback_query(F.data == "CANCEL_EM_SHUTDOWN")
async def cancel_shutdown(callback : CallbackQuery):
    await callback.message.edit_text("❌Экстренное перенаправление пользователей на другого админа отменено.")
    await sleep(1)
    await callback.message.delete()