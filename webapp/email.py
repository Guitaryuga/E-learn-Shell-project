from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread


mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[E-Learn-Shell] Сброс пароля',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.username],
               text_body=render_template('email/reset_password_mail.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password_mail.html',
                                         user=user, token=token))
