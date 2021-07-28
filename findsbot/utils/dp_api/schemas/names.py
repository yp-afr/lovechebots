from sqlalchemy import Column, BigInteger, String

from findsbot.utils.dp_api.database import db


class Names(db.Model):
    __tablename__ = 'finds_names'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)
    value = Column(String(2048))
    description = Column(String(2048))
