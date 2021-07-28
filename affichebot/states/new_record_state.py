from aiogram.dispatcher.filters.state import StatesGroup, State


class NewRecord(StatesGroup):
    ChooseCategory = State()
    ChooseSubcategory = State()
    EnterText = State()
    Media = State()