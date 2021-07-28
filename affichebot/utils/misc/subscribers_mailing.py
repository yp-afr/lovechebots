import logging

from aiogram.types import ParseMode

from affichebot.keyboards.inline.menu_keyboards import record_keyboard
from affichebot.loader import bot
from affichebot.utils.db_api.commands import get_subscribers, get_category_name_by_code, get_subcategory_name_by_code
from affichebot.utils.db_api.schemas.records import Records


async def subs_mailing(record: Records):
    bot.parse_mode = ParseMode.MARKDOWN
    category = record.category_name
    subcategory = record.subcategory_name

    category_name = await get_category_name_by_code(category)
    subcategory_name = await get_subcategory_name_by_code(subcategory)

    # если добавили запись без подкатегории

    if subcategory == "0":
        subscribers_all = await get_subscribers(category, "0")
        text = f"Новый пост!\n({category_name})\n\n{record.text}"
        for subscriber_all in subscribers_all:
            try:
                markup = await record_keyboard(record.id, subscriber_all.subscriber_id)
                if record.photo:
                    await bot.send_photo(chat_id=subscriber_all.subscriber_id, caption=text, photo=record.photo,
                                         reply_markup=markup)
                else:
                    await bot.send_message(chat_id=subscriber_all.subscriber_id, text=text, reply_markup=markup)
            except Exception as ex:
                logging.info(ex)
    else:
        subscribers_all = await get_subscribers(category, "0")
        subscribers = await get_subscribers(category, subcategory)
        text = f"Новый пост!\n({category_name})\n\n{record.text}"
        for subscriber_all in subscribers_all:
            try:
                markup = await record_keyboard(record.id, subscriber_all.subscriber_id)
                if record.photo:
                    await bot.send_photo(chat_id=subscriber_all.subscriber_id, caption=text, photo=record.photo,
                                         reply_markup=markup)
                else:
                    await bot.send_message(chat_id=subscriber_all.subscriber_id, text=text, reply_markup=markup)
            except Exception as ex:
                logging.info(ex)
        text = f"Новый пост!\n({category_name} - {subcategory_name})\n\n{record.text}"
        for subscriber in subscribers:
            try:
                markup = await record_keyboard(record.id, subscriber.subscriber_id)
                if record.photo:
                    await bot.send_photo(chat_id=subscriber.subscriber_id, caption=text, photo=record.photo,
                                         reply_markup=markup)
                else:
                    await bot.send_message(chat_id=subscriber.subscriber_id, text=text, reply_markup=markup)
            except Exception as ex:
                logging.warning(ex)

    bot.parse_mode = ParseMode.HTML
