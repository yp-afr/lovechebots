import logging

from aiogram import Bot
from aiogram import Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from .data import config
from .utils.db_api.database import db

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# storage = MemoryStorage()
storage = RedisStorage2('localhost', 6379, db=5)

bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

from affichebot import filters

filters.setup(dp)

__all__ = ["bot", "storage", "dp", "db"]
