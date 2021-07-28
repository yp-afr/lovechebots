import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from affichebot.filters import TextButton
from affichebot.filters.categories_text import IsCategory
from affichebot.keyboards.default.admin_keyboards import admin_keyboard
from affichebot.keyboards.default.menu_keyboards import text_categories_keyboard, text_subcategory_keyboard, \
    text_back_to_categories
from affichebot.keyboards.inline.menu_keyboards import subcategories_keyboard, menu_cd, record_keyboard, like_cd, \
    delete_cd, update_cd, whats_to_change_keyboard, updating_cd, back_subcategories_cd
from affichebot.loader import dp, bot
from affichebot.states.change_record_state import ChangeRecord
from affichebot.utils.db_api.commands import is_subcategories, get_category_code, get_records, put_like, \
    delete_record, add_subscriber, get_record, del_subscriber, store_click, get_subcategory_name_by_code, \
    get_category_name_by_code, is_unsubscribe, del_unsubscriber, add_unsubscriber, get_name


@dp.message_handler(TextButton("button_back_to_categories"), admin_check=True)
async def go_back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    messages = data.get("messages")
    if messages:
        for msg in messages:
            try:
                await bot.delete_message(types.User.get_current().id, msg)
            except Exception as ex:
                logging.info(ex)
    markup = await admin_keyboard()
    await message.answer(text=await get_name("menu_message"), reply_markup=markup)


@dp.message_handler(TextButton("button_back_to_categories"))
async def go_back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    messages = data.get("messages")
    if messages:
        for msg in messages:
            try:
                await bot.delete_message(types.User.get_current().id, msg)
            except Exception as ex:
                logging.info(ex)
    markup = await text_categories_keyboard()
    await message.answer(text=await get_name("menu_message"), reply_markup=markup)


@dp.message_handler(TextButton("button_subscribe_on_subcategory"))
async def subscribe_on(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category_code = data.get("category_code")
    subcategory_code = data.get("subcategory_code")
    if subcategory_code is None:
        subcategory_code = "0"
    try:
        result = await is_unsubscribe(category_code=category_code, subcategory_code=subcategory_code,
                                      chat_id=types.User.get_current().id)
        if result:
            await del_unsubscriber(category_code=category_code, subcategory_code=subcategory_code,
                                   unsubscriber_id=types.User.get_current().id)
        await add_subscriber(category_code=category_code, subcategory_code=subcategory_code,
                             subscriber_id=types.User.get_current().id)
        markup = await text_subcategory_keyboard(category_code, subcategory_code, types.User.get_current().id)
        value = await is_subcategories(category_code)
        category_name = await get_category_name_by_code(category_code)
        if value and (subcategory_code != "0"):
            subcategory_name = await get_subcategory_name_by_code(subcategory_code)
            await message.answer(f"{await get_name('subscribed_category_text')}{category_name} - {subcategory_name}",
                                 reply_markup=markup)
        else:
            await message.answer(f"{await get_name('subscribed_category_text')}{category_name}",
                                 reply_markup=markup)
    except Exception as ex:
        logging.warning(ex)


@dp.message_handler(TextButton("button_unsubscribe_from_subcategory"))
async def unsubscribe_from(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category_code = data.get("category_code")
    subcategory_code = data.get("subcategory_code")

    try:
        await del_subscriber(category_code, subcategory_code, types.User.get_current().id)
        await add_unsubscriber(category_code, subcategory_code, types.User.get_current().id)
        markup = await text_subcategory_keyboard(category_code, subcategory_code, types.User.get_current().id)
        value = await is_subcategories(category_code)
        category_name = await get_category_name_by_code(category_code)
        if value and (subcategory_code != "0"):
            subcategory_name = await get_subcategory_name_by_code(subcategory_code)
            await message.answer(f"{await get_name('unsubscribed_category_text')}{category_name} - {subcategory_name}",
                                 reply_markup=markup)
        else:
            await message.answer(f"{await get_name('unsubscribed_category_text')}{category_name}", reply_markup=markup)
    except Exception as ex:
        logging.warning(ex)


@dp.message_handler(IsCategory())
async def list_subcategories(message: types.Message, state: FSMContext):
    category = message.text
    category_code = await get_category_code(category)
    value = await is_subcategories(category_code)
    if value:
        markup = await text_back_to_categories()
        message_rpl = await message.answer(category, reply_markup=markup)
        markup = await subcategories_keyboard(category_code)
        message_inl = await message.answer(text=await get_name("choose_subcategory_text"), reply_markup=markup)
        await state.update_data(messages = [message_inl.message_id, message_rpl.message_id])
    else:
        markup = await text_subcategory_keyboard(category_code, "0", types.User.get_current().id)
        msg = await message.answer(text=await get_name("show_records_text"), reply_markup=markup)
        await state.update_data(messages=[msg.message_id])
        await show_records(None, category_code=category_code)
        await state.update_data(category_code=category_code, subcategory_code="0")


async def show_records(call: types.CallbackQuery, category_code, subcategory_code="0"):
    records = await get_records(category_code, subcategory_code)
    bot.parse_mode = "markdown"
    if call is not None:
        await call.message.delete()
    for record in records:
        markup = await record_keyboard(record.id, types.User.get_current().id)
        if record.photo:
            await bot.send_photo(photo=record.photo, caption=record.text, reply_markup=markup,
                                 disable_notification=True, chat_id=types.User.get_current().id)
        else:
            await bot.send_message(text=record.text, reply_markup=markup, disable_notification=True,
                                   chat_id=types.User.get_current().id)
        await asyncio.sleep(0.3)
    bot.parse_mode = "html"


@dp.callback_query_handler(back_subcategories_cd.filter(), admin_check=True)
async def go_back_to_categories(call: types.CallbackQuery):
    markup = await admin_keyboard()
    await call.message.answer(text=await get_name("menu_message"), reply_markup=markup)
    await call.message.delete()


@dp.callback_query_handler(back_subcategories_cd.filter(state="back_to_categories"))
async def go_back_to_categories(call: types.CallbackQuery):
    markup = await text_categories_keyboard()
    await call.message.answer(text=await get_name("menu_message"), reply_markup=markup)
    await call.message.delete()


@dp.callback_query_handler(menu_cd.filter())
async def get_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category_code = callback_data.get("cat_code")
    subcategory_code = callback_data.get("sub_code")
    markup = await text_subcategory_keyboard(category_code, subcategory_code, types.User.get_current().id)
    msg = await call.message.answer(text=await get_name("show_records_text"), reply_markup=markup)
    data = await state.get_data()
    msgs = data.get("messages")
    msgs.append(msg.message_id)
    await state.update_data(messages=msgs)
    await show_records(call, category_code, subcategory_code)
    await store_click(category_code, subcategory_code)
    await state.update_data(category_code=category_code, subcategory_code=subcategory_code)


@dp.callback_query_handler(like_cd.filter())
async def like_record(call: types.CallbackQuery, callback_data: dict):
    record_id = callback_data.get("record_id")
    await put_like(int(record_id))
    markup = await record_keyboard(int(record_id), types.User.get_current().id)
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(delete_cd.filter())
async def del_record(call: types.CallbackQuery, callback_data: dict):
    record_id = int(callback_data.get("record_id"))
    await delete_record(record_id)
    await call.message.delete()


@dp.callback_query_handler(update_cd.filter())
async def update_record(call: types.CallbackQuery, callback_data: dict):
    record_id = int(callback_data.get("record_id"))
    markup = await whats_to_change_keyboard(record_id)
    await call.message.reply(text=await get_name("whats_to_change_text"), reply_markup=markup)


@dp.callback_query_handler(updating_cd.filter(type="text"))
async def updating_text(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    record_id = int(callback_data.get("record_id"))
    await call.message.edit_text(text=await get_name("update_text_message"), reply_markup=None)
    await ChangeRecord.ChangeText.set()
    await state.update_data(record_id=record_id)


@dp.message_handler(content_types=types.ContentType.TEXT, state=ChangeRecord.ChangeText)
async def changing_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    record_id = data.get("record_id")
    record = await get_record(record_id)
    try:
        await record.update(text=message.text).apply()
        await message.answer(text=await get_name("text_successfully_updated"))
    except Exception as ex:
        logging.warning(ex)


@dp.callback_query_handler(updating_cd.filter(type="photo"))
async def updating_photo(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    record_id = int(callback_data.get("record_id"))
    await call.message.edit_text(text=await get_name("update_photo_message"), reply_markup=None)
    await ChangeRecord.ChangePhoto.set()
    await state.update_data(record_id=record_id)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=ChangeRecord.ChangePhoto)
async def changing_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    record_id = data.get("record_id")
    record = await get_record(record_id)
    photo = message.photo[-1].file_id
    try:
        await record.update(photo=photo).apply()
        await message.answer(text=await get_name("photo_successfully_updated"))
    except Exception as ex:
        logging.warning(ex)


@dp.callback_query_handler(updating_cd.filter(type="cancel"))
async def updating_cancel(call: types.CallbackQuery):
    await call.message.delete()
