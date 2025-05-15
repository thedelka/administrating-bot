import logging
from asyncio import run
from aiogram import Bot, Dispatcher
from Settings.get_config import config_manager
from Handlers.commands_handler import router as commands_handler_router
from Handlers.menu_handler import router as menu_handler_router
from Handlers.start_dialogue_handler import router as start_dialogue_handler_router
from Handlers.admin_dialogue_handler import router as dialogue_handler_router
from Handlers.admin_work_status_handler import router as admin_change_work_readiness_router
from Handlers.emergency_shutdown_handler import router as emergency_shutdown_handler_router
from Handlers.received_user_handler import router as show_user_history_handler_router


TOKEN = config_manager.get_config('BOT_CONSTANTS', 'TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

dp.include_routers(commands_handler_router, menu_handler_router,
                   start_dialogue_handler_router, dialogue_handler_router,
                   admin_change_work_readiness_router, emergency_shutdown_handler_router,
                   show_user_history_handler_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        run(main())

    except KeyboardInterrupt: pass
