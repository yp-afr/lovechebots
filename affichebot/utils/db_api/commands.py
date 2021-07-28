import logging
from typing import List

from sqlalchemy import and_

from affichebot.utils.db_api.schemas.admins import Admins
from affichebot.utils.db_api.schemas.categories import Categories
from affichebot.utils.db_api.schemas.names import Names
from affichebot.utils.db_api.schemas.records import Records
from affichebot.utils.db_api.schemas.stored_clicks import StoredClicks
from affichebot.utils.db_api.schemas.subcategories import Subcategories
from affichebot.utils.db_api.schemas.subscribed_users import Subscribers
from affichebot.utils.db_api.schemas.unsubscribe import Unsubscribe
from affichebot.utils.db_api.schemas.users import User


async def get_name(name_code):
    try:
        name = await Names.query.where(Names.name == name_code).gino.first()
        return name.value
    except Exception as ex:
        logging.info(ex)


async def get_subscribers(category_code, subcategory_code) -> List[Subscribers]:
    return await Subscribers.query.where(and_(Subscribers.category_code == category_code,
                                              Subscribers.subcategory_code == subcategory_code)).gino.all()


async def add_subscriber(category_code, subcategory_code, subscriber_id):
    subscriber = Subscribers()
    subscriber.category_code = category_code
    subscriber.subcategory_code = subcategory_code
    subscriber.subscriber_id = subscriber_id
    return await subscriber.create()


async def del_subscriber(category_code, subcategory_code, subscriber_id):
    return await Subscribers.delete.where(
        and_(Subscribers.category_code == category_code, Subscribers.subcategory_code == subcategory_code,
             Subscribers.subscriber_id == subscriber_id)).gino.status()


async def is_subscriber(category_code, subcategory_code, chat_id):
    return await Subscribers.query.where(
        and_(Subscribers.category_code == category_code, Subscribers.subcategory_code == subcategory_code,
             Subscribers.subscriber_id == chat_id)).gino.first()


async def is_unsubscribe(category_code, subcategory_code, chat_id):
    return await Unsubscribe.query.where(
        and_(Unsubscribe.category_code == category_code, Unsubscribe.subcategory_code == subcategory_code,
             Unsubscribe.unsubscriber_id == chat_id)).gino.first()


async def add_unsubscriber(category_code, subcategory_code, unsubscriber_id):
    unsubscriber = Unsubscribe()
    unsubscriber.category_code = category_code
    unsubscriber.subcategory_code = subcategory_code
    unsubscriber.unsubscriber_id = unsubscriber_id
    return await unsubscriber.create()


async def del_unsubscriber(category_code, subcategory_code, unsubscriber_id):
    return await Unsubscribe.delete.where(
        and_(Unsubscribe.category_code == category_code, Unsubscribe.subcategory_code == subcategory_code,
             Unsubscribe.unsubscriber_id == unsubscriber_id)).gino.status()


async def get_categories() -> List[Categories]:
    return await Categories.query.gino.all()


async def get_subcategories(category) -> List[Subcategories]:
    return await Subcategories.query.where(Subcategories.category_code == category).gino.all()


async def get_all_subcategories() -> List[Subcategories]:
    return await Subcategories.query.gino.all()


async def get_category_by_subcategory(subcategory):
    return await Subcategories.query.where(Subcategories.subcategory_name == subcategory).gino.first()


async def get_records(category, subcategory) -> List[Records]:
    records = await Records.query.where(
        and_(Records.category_name == category, Records.subcategory_name == subcategory)).gino.all()
    return records


async def get_record(record_id):
    return await Records.query.where(Records.id == record_id).gino.first()


async def put_like(record_id):
    try:
        record: Records = await get_record(record_id)
        likes: int
        likes = int(record.likes) + 1
        await record.update(likes=int(likes)).apply()
    except Exception as ex:
        print(ex)


async def store_click(category_code, subcategory_code):
    sc = StoredClicks(category_code=category_code, subcategory_code=subcategory_code)
    try:
        await sc.create()
    except Exception as ex:
        logging.info(ex)


async def is_subcategories(category):
    category_record: Categories = await Categories.query.where(Categories.category_code == category).gino.first()
    print(category_record)
    return category_record.is_subcategories


async def get_category_code(category_name):
    try:
        category: Categories = await Categories.query.where(Categories.category_name == category_name).gino.first()
        return category.category_code
    except Exception as ex:
        logging.info(ex)


async def get_category_name_by_code(category_code):
    try:
        category: Categories = await Categories.query.where(Categories.category_code == category_code).gino.first()
        return category.category_name
    except Exception as ex:
        logging.info(ex)


async def get_subcategory_name_by_code(subcategory_code):
    try:
        subcategory: Subcategories = await Subcategories.query.where(
            Subcategories.subcategory_code == subcategory_code).gino.first()
        return subcategory.subcategory_name
    except Exception as ex:
        logging.info(ex)


async def add_user(user_id: int):
    try:
        user = User(user_id=user_id)
        await user.create()
    except Exception as ex:
        logging.info(ex)


async def add_category(cat_name: str):
    try:
        cat = Categories(category_name=cat_name)
        await cat.create()
    except Exception as ex:
        logging.info(ex)


async def add_subcategory(cat_name: str, subcat_name: str):
    try:
        sub_cat = Subcategories(category_name=cat_name, subcategory_name=subcat_name)
        await sub_cat.create()
    except Exception as ex:
        logging.info(ex)


async def add_record(photo: str, text: str, category_name: str, subcategory_name: str):
    try:
        record = Records(photo=photo, text=text, category_name=category_name, subcategory_name=subcategory_name)
        await record.create()
    except Exception as ex:
        logging.info(ex)


async def delete_record(record_id):
    try:
        await Records.delete.where(Records.id == record_id).gino.status()
    except Exception as ex:
        logging.info(ex)


async def add_admin(phone, first_name, admin_id: str):
    admin = Admins(phone_number=phone, first_name=first_name, admin_id=admin_id)
    await admin.create()


async def get_all_admins():
    try:
        admins = await Admins.query.gino.all()
        return admins
    except Exception as ex:
        logging.info(ex)


async def del_admin(phone):
    try:
        await Admins.delete.where(Admins.phone_number == phone).gino.status()
    except Exception as ex:
        logging.info(ex)


async def get_admins() -> List:
    try:
        admins = await Admins.query.gino.all()
        ids = []
        for admin in admins:
            ids.append(int(admin.admin_id))
        return ids
    except Exception as ex:
        logging.info(ex)


async def get_all_users() -> List:
    try:
        users = await User.query.gino.all()
        ids = []
        for user in users:
            ids.append(user.user_id)
        return ids
    except Exception as ex:
        logging.info(ex)
