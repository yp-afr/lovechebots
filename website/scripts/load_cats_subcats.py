from website import db
from website.models import AfficheSubcategories, AfficheCategories


def get_categories():
    return db.session.query(AfficheCategories.category_name, AfficheCategories.category_code).order_by(
        AfficheCategories.category_name).all()


def get_subcategories_by_category_code(code):
    return db.session.query(AfficheSubcategories.subcategory_name, AfficheSubcategories.subcategory_code).filter(
        AfficheSubcategories.category_code == code).all()
