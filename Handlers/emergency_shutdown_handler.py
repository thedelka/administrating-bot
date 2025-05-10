from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, Bot

from Settings.get_config import config_manager

from Database.admins_data_db import admin_db_manager
from Database.users_data_db import user_db_manager

from asyncio import sleep

router = Router()

@router.callback_query(F.data == "CONFIRM_EM_SHUTDOWN")
async def confirm_shutdown(callback : CallbackQuery, bot : Bot):
    admin_id = callback.from_user.id
    user_ids_to_remove = admin_db_manager.admin_texting_user_id_operation(admin_id) #получение айди юзеров админа, нажавшего на кнопку

    await callback.message.answer("✅Экстренное перенаправление пользователей подтверждено. Все ваши пользователи:\n\n"
                                  f"{user_ids_to_remove}\n\nбыли переведены на свободного оператора.")
    await callback.message.delete()

    free_admin_id = config_manager.get_free_admin(admin_db_manager.get_db())

    print(f"[DEBUG] Айди свободного админа : {free_admin_id}")

    admin_db_manager.clear_admin_texting_user_id(admin_id) #удаляем всех юзеров у админа нажавшего на кнопку

    await bot.send_message(chat_id=free_admin_id, text=f"❗Оператор {admin_id} совершил экстренное отключение и передал вам свои обращения своих пользователей.\n\n"
                                          "Список переданных вам пользователей:")

    for user_id in user_ids_to_remove: #добавляем всех юзеров свободному админу
        admin_db_manager.admin_texting_user_id_operation(free_admin_id, user_id)
        await bot.send_message(chat_id=free_admin_id, text=f"{user_id} - {user_db_manager.get_username(user_id)}")

@router.callback_query(F.data == "CANCEL_EM_SHUTDOWN")
async def cancel_shutdown(callback : CallbackQuery):
    await callback.message.edit_text("❌Экстренное перенаправление пользователей на другого админа отменено.")
    await sleep(1)
    await callback.message.delete()