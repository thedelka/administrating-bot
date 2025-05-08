import logging, asyncio, json
from Settings.get_config import config_manager
from aiogram import Bot, Dispatcher
from Handlers.commands_handler import router as commands_handler_router
from Handlers.menu_handler import router as menu_handler_router
from Handlers.start_dialogue_handler import router as start_dialogue_handler_router
from Handlers.admin_dialogue_handler import router as dialogue_handler_router
from Handlers.admin_work_status_handler import router as admin_change_work_readiness_router

TOKEN = config_manager.get_config('BOT_CONSTANTS', 'TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

dp.include_routers(commands_handler_router, menu_handler_router, start_dialogue_handler_router, dialogue_handler_router, admin_change_work_readiness_router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Ошибка клавиатуры. Ничего страшного!")