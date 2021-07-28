from aiogram import types

markup = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Да", callback_data="yes"),
     types.InlineKeyboardButton(text="Нет", callback_data="no")]
])
