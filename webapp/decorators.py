from functools import wraps

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('У вас недостаточно прав для просмотра этой страницы')
            return redirect(url_for('material.index'))
        return func(*args, **kwargs)
    return decorated_view


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Пожалуйста, подтвердите аккаунт!', 'danger')
            return redirect(url_for('material.index'))
        return func(*args, **kwargs)
    return decorated_function
