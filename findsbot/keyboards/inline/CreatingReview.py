from aiogram import types

markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="ะะฐ ๐", callback_data="yes_review"),
         types.InlineKeyboardButton(text="ะะตั ๐", callback_data="no_review")]
    ]
)