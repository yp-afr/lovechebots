from aiogram import types

markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="Да 😄", callback_data="yes_review"),
         types.InlineKeyboardButton(text="Нет 😞", callback_data="no_review")]
    ]
)