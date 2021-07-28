from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from affichebot.utils.db_api.commands import get_categories, is_subscriber, get_name


async def text_categories_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    categories = await get_categories()
    for category in categories:
        if len(category.category_name) > 15:
            markup.row(category.category_name)
        else:
            markup.insert(KeyboardButton(text=category.category_name))

    return markup


async def text_subcategory_keyboard(cat_code, subcat_code, chat_id):
    value = await is_subscriber(category_code=cat_code, subcategory_code=subcat_code, chat_id=chat_id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if value:
        markup.insert(await get_name("button_unsubscribe_from_subcategory"))
    else:
        markup.insert(await get_name("button_subscribe_on_subcategory"))
    markup.insert(await get_name("button_back_to_categories"))
    return markup


async def text_back_to_categories():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_back_to_categories"))
    return markup

