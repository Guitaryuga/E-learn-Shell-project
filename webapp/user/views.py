import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from webapp.user.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from webapp.user.models import User
from webapp.db import db
from webapp.email import send_password_reset_email, send_confirmation_email
from webapp.token import confirm_token

blueprint = Blueprint('users', __name__, url_prefix='/users')

"""Роуты и функции, относящиеся к пользователю"""


@blueprint.route("/login")
def login():
    """Страница логина

    Если пользователь уже в системе, то его
    перенаправит на главную страницу.
    """
    if current_user.is_authenticated:
        return redirect(url_for("material.index"))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/signin.html', form=login_form,
                           page_title=title)


@blueprint.route("/logout")
def logout():
    """Функция логаута

    Если пользователь в зашел в систему, то он выйдет из нее,
    его перенаправит на главную страницу с оповещением о выходе.
    При попытке перейти на эту страницу неавторизованному пользователю,
    будет редирект на главную с оповещением.
    """
    if current_user.is_authenticated:
        logout_user()
        flash('Вы вышли из учетной записи', 'success')
        return redirect(url_for("material.index"))
    else:
        flash("Вам необходимо зарегистрироваться или войти", 'danger')
        return redirect(url_for("material.index"))


@blueprint.route("/process-login", methods=['POST'])
def process_login():
    """Функция процесса логина

    Если форма логина проходит валидацию, то пользователь входит в систему,
    его перенаправляет на главную страницу с оповещением.
    """
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


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    """Функция регистрации пользователя

    Если пользователь уже авторизован в системе,
    то при попытке попасть на страницу его перенаправит на главную.
    Если форма регистрации проходит валидацию, то указанные данные
    пользователя вносятся в БД и его переадресовывает на страницу логина
    """
    title = "Регистрация пользователя"
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('material.index'))
    if form.validate_on_submit():
        new_user = User(username=form.username.data, fio=form.fio.data,
                        company=form.company.data, position=form.position.data,
                        date_of_birth=form.date_of_birth.data,
                        phone_number=form.phone_number.data, role='user',
                        confirmed=False)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        send_confirmation_email(new_user)
        flash('Вы успешно зарегистрировались!Вам на почту отправлено письмо для подтверждения аккаунта', 'success')
        return redirect(url_for('users.login'))
    elif request.method == 'GET':
        form = RegistrationForm()
    else:
        flash('Пожалуйста, исправьте ошибки в форме')
    return render_template('user/registration.html', form=form,
                           page_title=title)


@blueprint.route("/confirm/<token>")
def confirm_email(token):
    """Функция подтверждения аккаунта

    Ссылка формируется с помощью токена для подтвреждения аккаунта,
    который втраивается в ссылку п письме для подтверждения аккаунта
    пользователя. Ссылка активна и действительна опр.количество времени.
    """
    try:
        email = confirm_token(token)
    except:
        flash('Ссылка для подтверждения неактивна', 'danger')
    user = User.query.filter_by(username=email).first_or_404()
    if user.confirmed:
        flash('Аккаунт уже подтвержден', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('Вы успешно подтвердили аккаунт, спасибо!', 'success')
    return redirect(url_for('users.login'))


@blueprint.route("/resend")
@login_required
def resend_confirmation():
    """Функция повторной отправки письма
    пользователю для подтвеждения аккаунта
    """
    send_confirmation_email(current_user)
    flash('Вам на почту отправлено письмо для подтверждения аккаунта', 'success')
    return redirect(url_for('material.index'))


@blueprint.route("/profile/<username>")
@login_required
def user(username):
    """Страница профиля пользователя"""
    profile = User.query.get(current_user.id)
    courses = profile.courses
    title = "Профиль"
    return render_template('user/profile.html', courses=courses,
                           page_title=title)


@blueprint.route("/profile/<username>/edit_profile", methods=['GET', 'POST'])
@login_required
def profile_edit(username):
    """Страница редактирования данных пользователя

    При переходе из профиля, пользователь попадает на страницу
    с формой, поля которой заполнены текущей информацией о нём.
    Её можно изменить по своему желанию и усмотрению, но с условием,
    что электронная почта и ФИО являются уникальными.
    """
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


@blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Страница с функцией запроса сброса пароля

    Ползователь вносит свой e-mail в форму и если форма проходит валидацию,
    то ему на почту приходит ссылка на страницу для сброса пароля.
    Если адреса нет в БД(пользователь не был зарегистрирован), то
    письмо не будет отправлено и появится предупреждение.
    """
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('На указанный адрес отправлено письмо с инструкциями', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_password_request.html',
                           title='Сброс пароля', form=form)


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Страница для сброса пароля и установления нового

    Пользователь переходит по ссылке присланной ему в письме,
    и если токен для сброса проходит верификацию, то попадает на
    страницу с формой для смены пароля. Если смена пароля проходит
    успешно, происходит перенаправление на страницу логина и оповещение
    о смене пароля.
    """
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('material.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменен', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_password.html', form=form)
