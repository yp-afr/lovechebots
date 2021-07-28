from sqlalchemy import Column, BigInteger, String, DateTime, Integer

from affichebot.utils.db_api.database import db

class Records(db.Model):
    __tablename__ = "affiche_records"

    id = Column(BigInteger, primary_key=True)
    photo = Column(String(1024))
    text = Column(String(3072))
    category_name = Column(String(64))
    subcategory_name = db.Column(db.String(64))
    likes = Column(Integer)
    posted = Column(DateTime(timezone=True), default=db.func.now())