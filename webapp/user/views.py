from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db

blueprint = Blueprint('users', __name__, url_prefix='/users')

'''
Вход-выход пользователя
'''


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("material.index"))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/signin.html', form=login_form,
                           page_title=title)


@blueprint.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Вы вышли из учетной записи', 'success')
        return redirect(url_for("material.index"))
    else:
        flash("Вам необходимо зарегистрироваться или войти", 'danger')
        return redirect(url_for("material.index"))


@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            login_user(user)
            flash('Вы вошли на сайт', 'success')
            return redirect(url_for("material.index"))
    flash('Неправильное пользователя или пароль', 'danger')
    return redirect(url_for("users.login"))


'''
Процесс регистрации пользователя
'''


@blueprint.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('material.index'))
    title = "Регистрация пользователя"
    form = RegistrationForm()
    return render_template('user/registration.html', form=form,
                           page_title=title)


@blueprint.route("/process-reg", methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, fio=form.fio.data,
                        company=form.company.data, position=form.position.data,
                        date_of_birth=form.date_of_birth.data,
                        phone_number=form.phone_number.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('users.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error, 'danger'))
        return redirect(url_for('users.register'))
    flash('Пожалуйста, исправьте ошибки в форме', 'danger')
    return redirect(url_for('users.register'))


'''
Профиль пользователя
'''


@blueprint.route("/profile/<username>")
@login_required
def user(username):
    profile = User.query.get(current_user.id)
    courses = profile.courses
    title = "Профиль"
    return render_template('user/profile.html', courses=courses,
                           page_title=title)
