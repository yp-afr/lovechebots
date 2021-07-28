from gino import Gino
from gino.schema import GinoSchemaVisitor

from affichebot.data import config

db = Gino()


async def on_startup():
    print("Бот Афиша: подключаюсь к базе данных")
    await db.set_bind(config.POSTGRES_URI)
    db.gino : GinoSchemaVisitor
