from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    texting = State()
    tired = State()