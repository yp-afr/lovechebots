from datetime import datetime, timedelta

from sqlalchemy import func

from website import db
from website.models import AfficheStoredClicks, AfficheSubcategories, AfficheCategories


def get_clicks():
    current_time = datetime.now()
    last_30d = current_time - timedelta(days=30)
    result = db.session.query(AfficheCategories.category_name,
                              AfficheSubcategories.subcategory_name,
                              func.count(AfficheStoredClicks.id)).filter(
        AfficheStoredClicks.date >= last_30d).join(AfficheCategories,
                                                   AfficheCategories.category_code == AfficheStoredClicks.category_code).join(
        AfficheSubcategories, AfficheSubcategories.subcategory_code == AfficheStoredClicks.subcategory_code).group_by(
        AfficheSubcategories.subcategory_name, AfficheCategories.category_name).order_by(
        func.count(AfficheStoredClicks.id).desc()).all()

    return result
