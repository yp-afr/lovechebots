from sqlalchemy import Column, BigInteger, String

from affichebot.utils.db_api.database import db


class Names(db.Model):
    __tablename__ = 'affiche_names'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)
    value = Column(String(2048))
    description = Column(String(2048))
