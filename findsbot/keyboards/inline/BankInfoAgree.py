from aiogram import types

markup = types.InlineKeyboardMarkup(
    inline_keyboard=[[
        types.InlineKeyboardButton(text="Зрозуміло", callback_data="agree")
    ]]
)
