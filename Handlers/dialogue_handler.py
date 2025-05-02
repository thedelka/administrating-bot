import json
from aiogram.fsm.context import FSMContext
from Settings.get_config import get_config
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram import Router, Bot, F
from States.dialogue_state import DialogueState

router = Router()

@router.callback_query(F.data.startswith("ANSWER"))
async def start_messaging(callback : CallbackQuery, state : FSMContext, bot : Bot):
    user_id = callback.data.split("_")[-1]
    operator_found_text = json.loads(get_config("MESSAGES", "found_not_taken_admin"))

    await bot.send_message(user_id, operator_found_text)

@router.message(StateFilter(DialogueState.dialogue_open))
async def send_user_messages_while_dialogue(message : Message, state : FSMContext):
    pass