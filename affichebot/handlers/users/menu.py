from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from affichebot.keyboards.default.admin_keyboards import admin_keyboard
from affichebot.keyboards.default.menu_keyboards import text_categories_keyboard
from affichebot.loader import dp, bot
from affichebot.utils.db_api.commands import get_name


@dp.message_handler(Command('menu'), admin_check=True, state="*")
async def list_categories_admin(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await admin_keyboard()
    await message.answer(text=await get_name("menu_message"), reply_markup=markup)


@dp.message_handler(Command('menu'), state="*")
async def list_categories(message: types.Message,state: FSMContext):
    await state.finish()
    markup = await text_categories_keyboard()
    user_id = message.from_user.id
    chat_id = "@lovechernihiv"
    try:
        result = await bot.get_chat_member(chat_id, user_id)
        if result['status'] == 'left':
            await message.answer(text=await get_name("unsubscribed_start"), reply_markup=None)
        else:
            await message.answer(text=await get_name("menu_message"), reply_markup=markup)
    except BadRequest:
        await message.answer(text=await get_name("unsubscribed_start"), reply_markup=None)
