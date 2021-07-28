from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from affichebot.utils.db_api.commands import get_categories, get_name


async def admin_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    categories = await get_categories()
    for category in categories:
        if len(category.category_name) > 15:
            markup.row(category.category_name)
        else:
            markup.insert(KeyboardButton(text=category.category_name))
    markup.row(await get_name("button_administration"))
    return markup


async def administration_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.insert(await get_name("button_create_new"))
    markup.insert(await get_name("button_mailing"))
    markup.insert(await get_name("button_add_admin"))
    markup.insert(await get_name("button_show_list_of_admins"))
    markup.row(await get_name("button_back_to_categories"))
    return markup


async def new_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_cancel"))
    return markup
