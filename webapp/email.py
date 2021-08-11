from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread
from webapp.token import generate_confirmation_token


mail = Mail()

"""Функции, отвечающие за отправку электронных писем"""


def send_async_email(app, msg):
    """Функция для отправки электронных писем в новом потоке"""
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    """Функция отправки электронных писем

    Принимает в качестве аргументов тему письма, отправителя, получателя,
    и html-шаблон письма. Создается объект thread для отправки сообщения
    в новом потоке.
    """
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """Функция отправки письма для сброса пароля

    Принимает в качестве аргумента пользователя,
    создает токен для сброса пароля и в письме отправляет
    сгенерированную ссылку для перехода и сброса пароля.
    """
    token = user.get_reset_password_token()
    send_email('[E-Learn-Shell] Сброс пароля',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.username],
               html_body=render_template('email/reset_password_mail.html',
                                         user=user, token=token))


def send_confirmation_email(new_user):
    """Функция отправка письма с подтверждением электронной почты.

    Принимает в качестве аргумента только созданного пользователя,
    создает токен подтверждения эл.адреса и генерирует ссылку для
    перехода и подтверждения
    """
    token = generate_confirmation_token(new_user.username)
    send_email('[E-Learn-Shell] Подтверждение аккаунта',
               sender=current_app.config['ADMINS'],
               recipients=[new_user.username],
               html_body=render_template('email/activate.html', token=token, new_user=new_user))
