from aiogram import Router, types, F

from Keyboards.admin_work_status_keyboard import get_work_status_kb
from Keyboards.emergency_shudown_keyboard import em_shut_kb_builder

from Database.admins_data_db import admin_db_manager

from Settings.get_config import config_manager

router = Router()

@router.message(F.text.in_(["Готов к работе", "Взять паузу"]))
async def change_admin_work_status(message: types.Message):
    admin_id = message.from_user.id

    print(f"У админа {admin_id} сейчас {admin_db_manager.admin_texting_user_id_operation(admin_id)} пользователей")

    current_status = admin_db_manager.get_admin_is_ready(admin_id)
    active_chats = admin_db_manager.admin_texting_user_id_operation(admin_id)

    if current_status and active_chats:
        return await send_warning_message(message)

    work_status_text = (config_manager.get_config("MESSAGES", "work_status_text_not_ready") if current_status
                        else config_manager.get_config("MESSAGES", "work_status_text_is_ready"))

    admin_db_manager.change_admin_is_ready(admin_id)

    await message.answer(text=work_status_text, reply_markup=get_work_status_kb(admin_db_manager.get_admin_is_ready(admin_id)))

    print(f"[DEBUG] Состояние админа: {admin_db_manager.get_admin_is_ready(admin_id)}")

async def send_warning_message(message : types.Message):
    await message.answer("❗Вы пытаетесь взять паузу, но у вас еще есть незавершённые диалоги с пользователями❗\n\n"
                         "Если вы нажмете \"✅Подтвердить\", все ваши обращения пользователей будут переведены на другого оператора❗",
                         reply_markup=em_shut_kb_builder.as_markup())


