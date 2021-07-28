from sqlalchemy import Column, BigInteger, String, DateTime

from affichebot.utils.db_api.database import db


class Subscribers(db.Model):
    __tablename__ = 'affiche_subscribers'
    id = Column(BigInteger, primary_key=True)
    category_code = Column(String(255))
    subcategory_code = Column(String(255))
    subscriber_id = Column(BigInteger)
    date = Column(DateTime(True), server_default=db.func.now())