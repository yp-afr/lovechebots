from flask_login import UserMixin

from . import db
from sqlalchemy.sql import func


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(512))
    password = db.Column(db.String(512))


class AfficheUser(db.Model):
    __tablename__ = 'affiche_users'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True)
    date = db.Column(db.DateTime(True), server_default=db.func.now())


class AfficheAdmins(db.Model):
    __tablename__ = "affiche_admins"

    id = db.Column(db.BigInteger, primary_key=True)
    admin_id = db.Column(db.String(1024))


class AfficheCategories(db.Model):
    __tablename__ = 'affiche_categories'
    id = db.Column(db.BigInteger, primary_key=True)
    category_name = db.Column(db.String(255))
    category_code = db.Column(db.String(255), unique=True)
    is_subcategories = db.Column(db.Boolean)


class AfficheNames(db.Model):
    __tablename__ = 'affiche_names'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    value = db.Column(db.String(2048))
    description = db.Column(db.String(2048))


class AfficheRecords(db.Model):
    __tablename__ = "affiche_records"

    id = db.Column(db.BigInteger, primary_key=True)
    photo = db.Column(db.String(1024))
    text = db.Column(db.String(3072))
    category_name = db.Column(db.String(64))
    subcategory_name = db.Column(db.String(64))
    likes = db.Column(db.Integer)
    posted = db.Column(db.DateTime(timezone=True), default=db.func.now())


class AfficheSubcategories(db.Model):
    __tablename__ = 'affiche_subcategories'
    id = db.Column(db.BigInteger, primary_key=True)
    category_code = db.Column(db.String(255))
    subcategory_name = db.Column(db.String(255))
    subcategory_code = db.Column(db.String(255), unique=True)


class AfficheSubscribers(db.Model):
    __tablename__ = 'affiche_subscribers'
    id = db.Column(db.BigInteger, primary_key=True)
    category_code = db.Column(db.String(255))
    subcategory_code = db.Column(db.String(255))
    subscriber_id = db.Column(db.BigInteger)
    date = db.Column(db.DateTime(True), server_default=db.func.now())


class AfficheStoredClicks(db.Model):
    __tablename__ = 'affiche_clicks'
    id = db.Column(db.BigInteger, primary_key=True)
    category_code = db.Column(db.String(500))
    subcategory_code = db.Column(db.String(500))
    date = db.Column(db.DateTime(True), server_default=db.func.now())


class AfficheUnsubscribe(db.Model):
    __tablename__ = 'affiche_unsubscribe'
    id = db.Column(db.BigInteger, primary_key=True)
    category_code = db.Column(db.String(255))
    subcategory_code = db.Column(db.String(255))
    unsubscriber_id = db.Column(db.BigInteger)
    date = db.Column(db.DateTime(True), server_default=db.func.now())


class FindsUser(db.Model):
    __tablename__ = 'finds_users'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True)
    date = db.Column(db.DateTime(True), server_default=db.func.now())


class FindsNames(db.Model):
    __tablename__ = 'finds_names'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    value = db.Column(db.String(2048))
    description = db.Column(db.String(2048))


class FindsRecords(db.Model):
    __tablename__ = "finds_records"

    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.BigInteger)
    author_username = db.Column(db.String(64))
    photo = db.Column(db.String(1024))
    caption = db.Column(db.String(3072))
    type = db.Column(db.String(64))
    category = db.Column(db.String(64))
    posted = db.Column(db.DateTime(timezone=True), default=db.func.now())