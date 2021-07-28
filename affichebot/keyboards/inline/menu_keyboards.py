from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from affichebot.utils.db_api.commands import get_subcategories, get_record, get_admins, get_name
from affichebot.utils.db_api.schemas.records import Records

menu_cd = CallbackData("show_records", "cat_code", "sub_code")
back_subcategories_cd = CallbackData("go_back", "state")


async def subcategories_keyboard(category):
    markup = InlineKeyboardMarkup(row_width=2)
    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        markup.insert(
            InlineKeyboardButton(text=subcategory.subcategory_name,
                                 callback_data=menu_cd.new(cat_code=category, sub_code=subcategory.subcategory_code))
        )
    markup.row(
        InlineKeyboardButton(text=f" - {await get_name('show_all_posts')} - ",
                             callback_data=menu_cd.new(cat_code=category, sub_code="0"))
    )
    return markup


like_cd = CallbackData("like", "record_id")
update_cd = CallbackData("update", "record_id")
delete_cd = CallbackData("delete", "record_id")
updating_cd = CallbackData("updating", "record_id", "type")


async def record_keyboard(record_id, user_id):
    markup = InlineKeyboardMarkup()
    record: Records = await get_record(record_id)
    text = "❤️" + str(record.likes)
    callback_data = like_cd.new(record_id=record.id)
    markup.insert(InlineKeyboardButton(text=text, callback_data=callback_data))
    text = await get_name("button_share_record")
    switch_text = "\n" + record.text
    markup.insert(InlineKeyboardButton(text=text, switch_inline_query=switch_text))
    admins = await get_admins()
    if int(user_id) in admins:
        markup.row(
            InlineKeyboardButton(text=await get_name("button_change_record"), callback_data=update_cd.new(record_id=record_id)),
            InlineKeyboardButton(text=await get_name("button_delete_record"), callback_data=delete_cd.new(record_id=record_id)))
    return markup


async def whats_to_change_keyboard(record_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text=await get_name("button_change_photo"),
                             callback_data=updating_cd.new(record_id=record_id, type="photo")),
        InlineKeyboardButton(text=await get_name("button_change_text"),
                             callback_data=updating_cd.new(record_id=record_id, type="text")))
    markup.row(
        InlineKeyboardButton(text=await get_name("button_cancel_updating_text"),
                             callback_data=updating_cd.new(record_id=record_id, type="cancel")))
    return markup
