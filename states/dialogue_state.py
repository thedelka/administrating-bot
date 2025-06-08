from aiogram.filters.state import State, StatesGroup


class DialogueState(StatesGroup):
    dialogue_open = State()
