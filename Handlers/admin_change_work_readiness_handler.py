from aiogram import Router, types
from Entities.admin import get_admin
router = Router()

@router.message(lambda message: message.text in ["Готов к работе", "Взять паузу"])
async def change_admin_work_status(message: types.Message):
    admin = get_admin(message.from_user.id)

    admin.is_ready_for_work = not admin.is_ready_for_work

    await message.answer("✅Вы готовы к работе. Ожидайте обращений пользователей." if admin.is_ready_for_work
                         else "🔚Вы не готовы к работе. К вам не будут поступать обращения пользователей.")