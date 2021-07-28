from aiogram import types
from aiogram.dispatcher import FSMContext

from affichebot.filters import TextButton
from affichebot.keyboards.default.admin_keyboards import admin_keyboard, administration_keyboard
from affichebot.keyboards.default.new_record_keyboards import new_record_cancel_keyboard, new_record_done_keyboard
from affichebot.keyboards.inline.new_record_keyboards import new_record_categories_keyboard, new_record_cd, \
    new_record_subcategories_keyboard, back_to_categories_new_record
from affichebot.loader import dp
from affichebot.states.new_record_state import NewRecord
from affichebot.utils.db_api.commands import get_category_code, is_subcategories
from affichebot.utils.db_api.schemas.records import Records
from affichebot.utils.misc.subscribers_mailing import subs_mailing


@dp.message_handler(TextButton("button_cancel"), state=NewRecord)
async def new_record(message: types.Message, state: FSMContext):
    await state.reset_state()
    markup = await administration_keyboard()
    await message.answer("Успешно отменено", reply_markup=markup)


@dp.message_handler(TextButton("button_done"), state=NewRecord.Media)
async def new_record(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    await state.reset_state()
    markup = await admin_keyboard()
    record = Records()
    record.likes = 1
    record.text = state_data.get("text")
    record.photo = state_data.get("photo")
    record.category_name = state_data.get("category_code")
    record.subcategory_name = state_data.get("subcategory_code")
    try:
        await record.create()
        await subs_mailing(record)
        await message.answer("Успешно!", reply_markup=markup)
    except Exception as ex:
        await message.answer(f"Произошла ошибка: {ex}")


@dp.message_handler(TextButton("button_create_new"))
async def new_record(message: types.Message, state: FSMContext):
    await state.reset_state()
    markup = await new_record_cancel_keyboard()
    await message.answer("<b>Создание нового поста</b>", reply_markup=markup)
    markup = await new_record_categories_keyboard()
    await message.answer("Выбери категорию", reply_markup=markup)
    await NewRecord.ChooseCategory.set()


@dp.callback_query_handler(back_to_categories_new_record.filter(state="new_record"), state=NewRecord)
async def go_back_to_categories_new_record(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    markup = await new_record_categories_keyboard()
    await call.message.edit_reply_markup(reply_markup=markup)
    await NewRecord.ChooseCategory.set()


@dp.callback_query_handler(new_record_cd.filter(), state=NewRecord.ChooseCategory)
async def get_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category = await get_category_code(callback_data.get('category'))
    value = await is_subcategories(category=category)
    if value:
        markup = await new_record_subcategories_keyboard(category)
        await call.message.edit_text("Выбери подкатегорию", reply_markup=markup)
        await NewRecord.ChooseSubcategory.set()
    else:
        await call.message.edit_text("Введи текст:")
        await NewRecord.EnterText.set()
        await state.update_data(category_code=category, subcategory_code="0")


@dp.callback_query_handler(new_record_cd.filter(), state=NewRecord.ChooseSubcategory)
async def get_subcategory(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category_code = callback_data.get('category')
    subcategory_code = callback_data.get('subcategory')
    await call.message.edit_reply_markup()
    await call.message.edit_text("Введи текст:")
    await NewRecord.EnterText.set()
    await state.update_data(category_code=category_code, subcategory_code=subcategory_code)


@dp.message_handler(state=NewRecord.EnterText)
async def get_text(message: types.Message, state: FSMContext):
    text = message.text
    markup = await new_record_done_keyboard()
    await message.answer("Отлично, теперь отправь фото", reply_markup=markup)
    await NewRecord.Media.set()
    await state.update_data(text=text)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=NewRecord.Media)
async def get_media(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
