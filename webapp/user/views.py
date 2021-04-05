from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from webapp.user.forms import LoginForm, RegistrationForm, EditProfileForm
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


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    title = "Регистрация пользователя"
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('material.index'))
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
    elif request.method == 'GET':
        form = RegistrationForm()
    else:
        flash('Пожалуйста, исправьте ошибки в форме')
    return render_template('user/registration.html', form=form,
                           page_title=title)


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


@blueprint.route("/profile/<username>/edit_profile", methods=['GET', 'POST'])
@login_required
def profile_edit(username):
    user = User.query.get(current_user.id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.fio = form.fio.data
        current_user.company = form.company.data
        current_user.position = form.position.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Изменения успешно сохранены', 'success')
        return redirect(url_for('users.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fio.data = current_user.fio
        form.company.data = current_user.company
        form.position.data = current_user.position
        form.date_of_birth.data = current_user.date_of_birth
        form.phone_number.data = current_user.phone_number
    else:
        flash('Ошибка при редактировании данных', 'danger')
    return render_template('user/edit_profile.html', page_title='Редактирование профиля',
                           form=form)
