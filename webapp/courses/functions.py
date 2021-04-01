from urllib.parse import urlparse, urljoin

from flask import request, flash
from flask_login import current_user

from webapp.db import db
from webapp.user.models import User_answer


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http', 'https')
            and ref_url.netloc == test_url.netloc)


'''
Модификация для request.referrer, для проверки безопасности url
'''


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


'''
Внутренняя функция проверки ответов в тесте
и занесения ответа пользователя в БД
'''


def checking_answer(correct_answer, answer_value, question_id,
                    lesson_id, lesson_name, course_id):
    if correct_answer == answer_value:
        answer_status = "correct"
        answer = User_answer(answer_status=answer_status,
                             question_id=question_id,
                             user_answer=answer_value,
                             user_id=current_user.id,
                             course_id=course_id,
                             lesson_id=lesson_id,
                             lesson_name=lesson_name)
        db.session.add(answer)
        db.session.commit()
        flash('Вы дали верный ответ', 'success')
    else:
        answer_status = "wrong"
        answer = User_answer(answer_status=answer_status,
                             question_id=question_id,
                             user_answer=answer_value,
                             user_id=current_user.id,
                             course_id=course_id,
                             lesson_id=lesson_id,
                             lesson_name=lesson_name)
        db.session.add(answer)
        db.session.commit()
        flash("Ответ неверный", "danger")
