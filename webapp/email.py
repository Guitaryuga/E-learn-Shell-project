from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread
from webapp.token import generate_confirmation_token


mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[E-Learn-Shell] Сброс пароля',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.username],
               html_body=render_template('email/reset_password_mail.html',
                                         user=user, token=token))


def send_confirmation_email(new_user):
    token = generate_confirmation_token(new_user.username)
    send_email('[E-Learn-Shell] Подтверждение аккаунта',
               sender=current_app.config['ADMINS'][0],
               recipients=[new_user.username],
               html_body=render_template('email/activate.html', token=token, new_user=new_user))
