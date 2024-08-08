from aiogram.fsm.state import State, StatesGroup


class ChatSurvey(StatesGroup):
    model = State()
    query = State()
    wait = State()
