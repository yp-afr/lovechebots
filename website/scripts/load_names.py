from website import db
from website.models import AfficheNames, FindsNames


def get_names_affiche():
    return db.session.query(AfficheNames.id, AfficheNames.description, AfficheNames.value).order_by(
        AfficheNames.id.asc()).all()


def get_names_finds():
    return db.session.query(FindsNames.id, FindsNames.description, FindsNames.value).all()
