from urllib.parse import urlparse, urljoin

from flask import request, flash, redirect
from flask_login import current_user

from webapp.model import db, User_answer, Question


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():  # модификация для request.referrer, для проверки безопасности url
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def checking_answer(correct_answer, answer_value, question_id):  # внутренняя функция проверки ответов в тесте и занесения ответа пользователя в БД
    if correct_answer == answer_value:
        answer_status = "correct"
        answer = User_answer(answer_status=answer_status, question_id=question_id, user_answer=answer_value, user_id=current_user.id)
        db.session.add(answer)
        db.session.commit()
        flash('Вы дали верный ответ', 'success')
    else:
        flash("Ответ неверный", "danger")
