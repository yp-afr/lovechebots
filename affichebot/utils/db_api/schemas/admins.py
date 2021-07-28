from sqlalchemy import Column, BigInteger, String, sql

from affichebot.utils.db_api.database import db


class Admins(db.Model):
    __tablename__ = "affiche_admins"

    id = Column(BigInteger, primary_key=True)
    phone_number = Column(String(64), unique=True)
    first_name = Column(String(512))
    admin_id = Column(String(1024))

    query: sql.Select
