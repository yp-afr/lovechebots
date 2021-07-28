import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from findsbot.filters import TextButton
from findsbot.keyboards.default.Administration import administration
from findsbot.keyboards.default.main_menus import admin_main_menu
from findsbot.keyboards.inline.administration_funcs import contact_keyboard, new_admin_keyboard, delete_admin_cd
from findsbot.loader import dp
from findsbot.states.AddingAdmin import AddingAdmin
from findsbot.utils.dp_api.commands import get_all_admins, add_admin, del_admin, get_name


@dp.message_handler(TextButton("button_admin_text"), admin_check=True)
async def admin(message: types.Message):
    markup = await administration()
    await message.answer("Меню администратора: ", reply_markup=markup)


@dp.message_handler(TextButton("button_back_to_main_menu"))
async def go_back_to_main_menu(message: types.Message):
    markup = await admin_main_menu()
    await message.answer(text=await get_name("menu_text"), reply_markup=markup)


@dp.message_handler(TextButton("button_show_list_of_admins"), admin_check=True)
async def show_admins(message: types.Message):
    admins = await get_all_admins()
    if admins:
        for adm in admins:
            try:
                markup = await contact_keyboard(adm.phone_number)
                await message.answer_contact(adm.phone_number, adm.first_name, reply_markup=markup)
            except Exception as ex:
                logging.error(ex)
    else:
        await message.answer("Список назначенных админов пуст!")


@dp.message_handler(TextButton("button_cancel_text"), state=AddingAdmin)
async def cancel_adding(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await administration()
    await message.answer("Отменено!", reply_markup=markup)


@dp.message_handler(TextButton("button_add_admin"), admin_check=True)
async def add_administrator(message: types.Message):
    markup = await new_admin_keyboard()
    await message.answer("""Для добавления администратора необходимо отправить его контакт
(📎 -> Контакт)""", reply_markup=markup)
    await AddingAdmin.SendContact.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=AddingAdmin.SendContact)
async def getting_contact(message: types.Message, state: FSMContext):
    try:
        await add_admin(phone=message.contact.phone_number, first_name=message.contact.first_name,
                        admin_id=str(message.contact.user_id))
        markup = await administration()
        await message.answer("Новый администратор успешно добавлен!", reply_markup=markup)
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Ошибка добавления!", reply_markup=markup)
        logging.error(ex)
    await state.finish()


@dp.callback_query_handler(delete_admin_cd.filter())
async def deleting_admin(call: types.CallbackQuery, callback_data: dict):
    phone = callback_data.get("phone_number")
    await del_admin(phone)
    await call.message.delete()
