from aiogram import types
from aiogram.utils.callback_data import CallbackData

from findsbot.utils.dp_api.commands import get_name

types_cd = CallbackData("type", "value")
categories_cd = CallbackData("category", "value")
new_post_types_cd = CallbackData("type", "value")


async def categories_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=await get_name("button_docs"), callback_data=categories_cd.new("Документы"))],
        [types.InlineKeyboardButton(text=await get_name("button_technic"), callback_data=categories_cd.new("Техника"))],
        [types.InlineKeyboardButton(text=await get_name("button_keys"), callback_data=categories_cd.new("Ключи"))],
        [types.InlineKeyboardButton(text=await get_name("button_handbags"), callback_data=categories_cd.new("Кошельки/Сумки"))],
        [types.InlineKeyboardButton(text=await get_name("button_pets"), callback_data=categories_cd.new("Питомцы"))],
        [types.InlineKeyboardButton(text=await get_name("button_else"), callback_data=categories_cd.new("Другое"))],
        [types.InlineKeyboardButton(text=await get_name("button_back"), callback_data=categories_cd.new("Назад"))],
    ])
    return markup


async def types_keyboard():
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=await get_name("button_found"),
                                        callback_data=types_cd.new(await get_name("button_found"))),
             types.InlineKeyboardButton(text=await get_name("button_lost"),
                                        callback_data=types_cd.new(await get_name("button_lost")))]
        ]
    )
    return markup


async def new_post_types_keyboard():
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=await get_name("button_finds"),
                                        callback_data=new_post_types_cd.new(await get_name("button_found"))),
             types.InlineKeyboardButton(text=await get_name("button_losts"),
                                        callback_data=new_post_types_cd.new(await get_name("button_lost")))]
        ]
    )
    return markup


async def with_bank_categories_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=await get_name("button_docs"), callback_data=categories_cd.new("Документы"))],
        [types.InlineKeyboardButton(text=await get_name("button_technic"), callback_data=categories_cd.new("Техника"))],
        [types.InlineKeyboardButton(text=await get_name("button_keys"), callback_data=categories_cd.new("Ключи"))],
        [types.InlineKeyboardButton(text=await get_name("button_handbags"),
                                    callback_data=categories_cd.new("Кошельки/Сумки"))],
        [types.InlineKeyboardButton(text=await get_name("button_pets"), callback_data=categories_cd.new("Питомцы"))],
        [types.InlineKeyboardButton(text=await get_name("button_bank"), callback_data=categories_cd.new("Bank"))],
        [types.InlineKeyboardButton(text=await get_name("button_else"), callback_data=categories_cd.new("Другое"))],
        [types.InlineKeyboardButton(text=await get_name("button_back"), callback_data=categories_cd.new("Назад"))],
    ])
    return markup
