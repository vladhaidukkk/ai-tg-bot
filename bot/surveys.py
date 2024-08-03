from aiogram.fsm.state import State, StatesGroup


class ChatSurvey(StatesGroup):
    query = State()
    wait = State()
