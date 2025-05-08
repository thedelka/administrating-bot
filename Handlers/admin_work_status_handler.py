from aiogram import Router, types
from Settings.get_config import config_manager
from Keyboards.admin_work_status_keyboard import get_work_status_kb
router = Router()

@router.message()
async def change_admin_work_status(message: types.Message):
    admin = config_manager.get_admin(message.from_user.id)

    admin.is_ready = not admin.is_ready

    await message.answer("✅Вы готовы к работе. Ожидайте обращений пользователей." if admin.is_ready
                         else "🔚Вы не готовы к работе. К вам не будут поступать обращения пользователей.", reply_markup=get_work_status_kb(admin.is_ready))
