import asyncio

from affichebot.data import config
from affichebot.loader import bot
from affichebot.utils.db_api import database


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(chat_id=config.SUPERUSER, text="Я запущен!")
    # from affichebot.utils.db_api.database import db
    # await db.gino.create_all()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(database.on_startup())
    from aiogram import executor
    from affichebot.handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
