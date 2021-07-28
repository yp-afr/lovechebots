from sqlalchemy import Column, BigInteger, DateTime

from affichebot.utils.db_api.database import db


class User(db.Model):
    __tablename__ = 'affiche_users'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    date = Column(DateTime(True), server_default=db.func.now())
