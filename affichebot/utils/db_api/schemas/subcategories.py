from sqlalchemy import Column, BigInteger, String

from affichebot.utils.db_api.database import db


class Subcategories(db.Model):
    __tablename__ = 'affiche_subcategories'
    id = Column(BigInteger, primary_key=True)
    category_code = Column(String(255))
    subcategory_name = Column(String(255))
    subcategory_code = Column(String(255), unique=True)
