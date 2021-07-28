from aiogram import types
from aiogram.dispatcher.filters import Filter

from affichebot.utils.db_api.commands import get_categories, get_all_subcategories


class IsCategory(Filter):
    key = "is_category"

    async def check(self, message: types.Message):
        list_categories = []
        categories = await get_categories()
        for category in categories:
            list_categories.append(category.category_name)
        return message.text in list_categories
