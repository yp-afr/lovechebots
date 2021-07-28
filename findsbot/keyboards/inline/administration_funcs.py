from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from findsbot.utils.dp_api.commands import get_name

delete_admin_cd = CallbackData("del_admin", "phone_number")


async def contact_keyboard(phone_number):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Снять", callback_data=delete_admin_cd.new(phone_number=phone_number)))
    return markup


async def new_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_cancel_text"))
    return markup
