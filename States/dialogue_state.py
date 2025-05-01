from aiogram.filters.state import State, StatesGroup

class DialogueState(StatesGroup):
    dialogue_open = State()
    dialogue_not_open = State()