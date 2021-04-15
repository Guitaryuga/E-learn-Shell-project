from itsdangerous import URLSafeSerializer
from flask import current_app


def generate_confirmation_token(email):
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                                 salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except:
        return False
    return email
