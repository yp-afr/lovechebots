import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from affichebot.filters import TextButton
from affichebot.keyboards.default.admin_keyboards import administration_keyboard, new_admin_keyboard
from affichebot.keyboards.inline.administration import contact_keyboard, delete_admin_cd
from affichebot.loader import dp
from affichebot.states.adding_admin import AddingAdmin
from affichebot.utils.db_api.commands import add_admin, get_all_admins, del_admin


@dp.message_handler(TextButton("button_administration"), admin_check=True)
async def administration(message: types.Message):
    markup = await administration_keyboard()
    await message.answer("Меню администратора:", reply_markup=markup)


@dp.message_handler(TextButton("button_show_list_of_admins"), admin_check=True)
async def show_admins(message: types.Message):
    admins = await get_all_admins()
    if admins:
        for admin in admins:
            try:
                markup = await contact_keyboard(admin.phone_number)
                await message.answer_contact(admin.phone_number, admin.first_name, reply_markup=markup)
            except Exception as ex:
                logging.info(ex)
    else:
        await message.answer("Список назначенных админов пуст!")


@dp.message_handler(TextButton("button_add_admin"), admin_check=True)
async def add_administrator(message: types.Message):
    markup = await new_admin_keyboard()
    await message.answer("""Для добавления администратора необходимо отправить его контакт
(📎 -> Контакт)""", reply_markup=markup)
    await AddingAdmin.SendContact.set()


@dp.message_handler(TextButton("button_cancel"), state=AddingAdmin)
async def cancel_adding(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await administration_keyboard()
    await message.answer("Отменено!", reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=AddingAdmin.SendContact)
async def getting_contact(message: types.Message, state: FSMContext):
    markup = await administration_keyboard()
    try:
        await add_admin(phone=message.contact.phone_number, first_name=message.contact.first_name,
                        admin_id=str(message.contact.user_id))
        await message.answer("Новый администратор успешно добавлен!", reply_markup=markup)
    except Exception as ex:
        await message.answer(f"Ошибка добавления!", reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(delete_admin_cd.filter())
async def deleting_admin(call: types.CallbackQuery, callback_data: dict):
    phone = callback_data.get("phone_number")
    await del_admin(phone)
    await call.message.delete()
