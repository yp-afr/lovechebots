from sqlalchemy import func

from website import db
from website.models import AfficheUnsubscribe, AfficheCategories, AfficheSubcategories


def get_unsubscribe():
    result_categories = db.session.query(AfficheCategories.category_name, func.count(AfficheUnsubscribe.id)).filter(
        AfficheUnsubscribe.subcategory_code == "0").join(
        AfficheCategories, AfficheUnsubscribe.category_code == AfficheCategories.category_code).group_by(
        AfficheCategories.category_name).all()
    result_with_subcategories = db.session.query(AfficheCategories.category_name, AfficheSubcategories.subcategory_name,
                                                 func.count(AfficheUnsubscribe.id)).join(AfficheCategories,
                                                                                         AfficheUnsubscribe.category_code == AfficheCategories.category_code).join(
        AfficheSubcategories, AfficheUnsubscribe.subcategory_code == AfficheSubcategories.subcategory_code).group_by(
        AfficheCategories.category_name, AfficheSubcategories.subcategory_name).all()
    return result_categories, result_with_subcategories
