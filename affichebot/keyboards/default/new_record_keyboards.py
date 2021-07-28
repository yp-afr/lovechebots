from aiogram.types import ReplyKeyboardMarkup

from affichebot.utils.db_api.commands import get_name


async def new_record_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_cancel"))
    return markup


async def new_record_done_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_done"))
    markup.insert(await get_name("button_cancel"))
    return markup
