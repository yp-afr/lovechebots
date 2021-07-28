from datetime import datetime, timedelta
from typing import Tuple

from sqlalchemy import func

from website import db
from website.models import AfficheUser, FindsUser


def get_new_users_info_affiche() -> Tuple:
    current_time = datetime.now()
    last_24h = current_time - timedelta(days=1)
    last_7d = current_time - timedelta(days=7)
    last_30d = current_time - timedelta(days=30)
    day = func.to_char(AfficheUser.date, 'dd.mm')
    rows_count = []
    row1_count_all = db.session.query(func.count(AfficheUser.user_id)).filter(
        AfficheUser.date >= last_24h).scalar()
    rows_count.append(row1_count_all)
    rows7_count_all = db.session.query(func.count(AfficheUser.user_id)).filter(
        AfficheUser.date >= last_7d).scalar()
    rows_count.append(rows7_count_all)
    rows30_count_all = db.session.query(func.count(AfficheUser.user_id)).filter(
        AfficheUser.date >= last_30d).scalar()
    rows_count.append(rows30_count_all)
    row1 = db.session.query(func.to_char(AfficheUser.date, 'HH24:00'), func.count(AfficheUser.user_id)).filter(
        AfficheUser.date >= last_24h).group_by(
        AfficheUser.date).order_by(func.to_char(AfficheUser.date, 'HH24:00').desc()).all()
    rows7 = db.session.query(day.label('x'), func.count(AfficheUser.user_id).label('y')).filter(
        AfficheUser.date >= last_7d).group_by(
        day).order_by(day.desc()).all()

    rows30 = db.session.query(day.label('x'), func.count(AfficheUser.user_id).label('y')).filter(
        AfficheUser.date >= last_30d).group_by(
        day).order_by(day.desc()).all()

    row1.reverse()
    rows7.reverse()
    rows30.reverse()
    return dict(row1), dict(rows7), dict(rows30), rows_count


def get_new_users_info_finds() -> Tuple:
    current_time = datetime.now()
    last_24h = current_time - timedelta(days=1)
    last_7d = current_time - timedelta(days=7)
    last_30d = current_time - timedelta(days=30)
    day = func.to_char(FindsUser.date, 'dd.mm')
    rows_count = []
    row1_count_all = db.session.query(func.count(FindsUser.user_id)).filter(
        FindsUser.date >= last_24h).scalar()
    rows_count.append(row1_count_all)
    rows7_count_all = db.session.query(func.count(FindsUser.user_id)).filter(
        FindsUser.date >= last_7d).scalar()
    rows_count.append(rows7_count_all)
    rows30_count_all = db.session.query(func.count(FindsUser.user_id)).filter(
        FindsUser.date >= last_30d).scalar()
    rows_count.append(rows30_count_all)
    row1 = db.session.query(func.to_char(FindsUser.date, 'HH24:00'), func.count(FindsUser.user_id)).filter(
        FindsUser.date >= last_24h).group_by(
        FindsUser.date).order_by(func.to_char(FindsUser.date, 'HH24:00').desc()).all()
    rows7 = db.session.query(day.label('x'), func.count(FindsUser.user_id).label('y')).filter(
        FindsUser.date >= last_7d).group_by(
        day).order_by(day.desc()).all()

    rows30 = db.session.query(day.label('x'), func.count(FindsUser.user_id).label('y')).filter(
        FindsUser.date >= last_30d).group_by(
        day).order_by(day.desc()).all()

    row1.reverse()
    rows7.reverse()
    rows30.reverse()
    return dict(row1), dict(rows7), dict(rows30), rows_count
