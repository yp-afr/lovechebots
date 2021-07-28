from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

delete_admin_cd = CallbackData("del_admin", "phone_number")


async def contact_keyboard(phone_number):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Снять", callback_data=delete_admin_cd.new(phone_number=phone_number)))
    return markup
