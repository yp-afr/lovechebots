from sqlalchemy import Column, BigInteger, DateTime, String

from affichebot.utils.db_api.database import db


class StoredClicks(db.Model):
    __tablename__ = 'affiche_clicks'
    id = Column(BigInteger, primary_key=True)
    category_code = Column(String(500))
    subcategory_code = Column(String(500))
    date = Column(DateTime(True), server_default=db.func.now())
