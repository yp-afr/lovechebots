from datetime import datetime, timedelta
from typing import Tuple

from sqlalchemy import func

from website import db
from website.models import FindsRecords


def get_creating_posts_stats():
    current_time = datetime.now()
    last_30d = current_time - timedelta(days=30)
    day = func.to_char(FindsRecords.posted, 'dd.mm')

    rows30 = db.session.query(day, func.count(FindsRecords.id)).filter(
        FindsRecords.posted >= last_30d).group_by(
        day).order_by(day.desc()).all()

    rows30.reverse()

    return dict(rows30)
