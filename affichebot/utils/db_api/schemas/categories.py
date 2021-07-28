from sqlalchemy import Column, BigInteger, String, Boolean

from affichebot.utils.db_api.database import db


class Categories(db.Model):
    __tablename__ = 'affiche_categories'
    id = Column(BigInteger, primary_key=True)
    category_name = Column(String(255))
    category_code = Column(String(255), unique=True)
    is_subcategories = Column(Boolean)
