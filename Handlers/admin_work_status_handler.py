from aiogram import Router, types, F

from Keyboards.admin_work_status_keyboard import get_work_status_kb

from Database.admins_data_db import admin_db_manager

router = Router()

@router.message(F.text.in_(["Готов к работе", "Взять паузу"]))
async def change_admin_work_status(message: types.Message):
    admin_db_manager.change_admin_is_ready(message.from_user.id)

    await message.answer("✅Вы готовы к работе. Ожидайте обращений пользователей." if admin_db_manager.get_admin_is_ready(message.from_user.id)
                         else "🔚Вы не готовы к работе. К вам не будут поступать обращения пользователей.",
                         reply_markup=get_work_status_kb(admin_db_manager.get_admin_is_ready(message.from_user.id)))

    print(f"[DEBUG] Состояние админа: {admin_db_manager.get_admin_is_ready(message.from_user.id)}")