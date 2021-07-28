from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeRecord(StatesGroup):
    ChangePhoto = State()
    ChangeText = State()
