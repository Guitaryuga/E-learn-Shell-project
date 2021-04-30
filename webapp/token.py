from itsdangerous import URLSafeSerializer
from flask import current_app


def generate_confirmation_token(email):
    """Функция генерации токена для подтверждения e-mail

    Принимает в качестве аргумента e-mail пользователя, возвращает
    созданный токен.
    """
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    """Функция проверки токена

    Принимает в качестве аргумента токен и время его действия,
    в случае если срок действия не истек, возвращает e-mail
    пользователя для дальнейшей проверки.
    """
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                                 salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except:
        return False
    return email
