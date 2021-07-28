from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from affichebot.utils.db_api.commands import get_categories, get_subcategories, get_name

new_record_cd = CallbackData("new_record", "category", "subcategory")
back_to_categories_new_record = CallbackData("go_back", "state")


def make_callback_data(category, subcategory="0"):
    return new_record_cd.new(category=category, subcategory=subcategory)


async def new_record_categories_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    categories = await get_categories()
    for category in categories:
        button_text = category.category_name
        callback_data = make_callback_data(category=category.category_name)
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup


async def new_record_subcategories_keyboard(category):
    markup = InlineKeyboardMarkup(row_width=2)
    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        button_text = subcategory.subcategory_name
        callback_data = make_callback_data(category=category, subcategory=subcategory.subcategory_code)
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    markup.row(InlineKeyboardButton(text=await get_name("button_go_back"),
                                    callback_data=back_to_categories_new_record.new("new_record")))
    return markup
