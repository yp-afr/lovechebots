from sqlalchemy import func

from website import db
from website.models import AfficheSubscribers, AfficheCategories, AfficheSubcategories


def get_subscriptions():
    result_categories = db.session.query(AfficheCategories.category_name, func.count(AfficheSubscribers.id)).filter(
        AfficheSubscribers.subcategory_code == "0").join(
        AfficheCategories, AfficheSubscribers.category_code == AfficheCategories.category_code).group_by(
        AfficheCategories.category_name).all()
    result_with_subcategories = db.session.query(AfficheCategories.category_name, AfficheSubcategories.subcategory_name,
                                                 func.count(AfficheSubscribers.id)).join(AfficheCategories,
                                                                                         AfficheSubscribers.category_code == AfficheCategories.category_code).join(
        AfficheSubcategories, AfficheSubscribers.subcategory_code == AfficheSubcategories.subcategory_code).group_by(
        AfficheCategories.category_name, AfficheSubcategories.subcategory_name).all()
    return result_categories, result_with_subcategories
