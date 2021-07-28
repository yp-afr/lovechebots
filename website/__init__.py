import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v8y/B?E(H+MbQeShVmYq3t6w9z$C&F)J@N'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:example@192.168.99.100:5432/postgres"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import Users

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    # from .models import AfficheCategories, AfficheSubCategories

    # create_users(app)

    return app


def create_users(app):
    db.create_all(app=app)
    print("Created!")
