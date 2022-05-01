from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from .models import Users


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user:
            print(generate_password_hash(password))
            if check_password_hash(user.password, password):
                flash('Успешно!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.bots'))
            else:
                flash('Неверное имя пользователя или пароль!', category='error')

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
