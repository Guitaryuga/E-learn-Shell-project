from urllib.parse import urlparse, urljoin

from flask import request, flash, redirect, url_for, current_app
from flask_login import current_user, config
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField
from webapp.decorators import admin_required

from webapp.model import db, User_answer, Question


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# модификация для request.referrer, для проверки безопасности url
def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


# внутренняя функция проверки ответов в тесте и занесения ответа пользователя в БД
def checking_answer(correct_answer, answer_value, question_id, lesson_id, lesson_name):
    if correct_answer == answer_value:
        answer_status = "correct"
        answer = User_answer(answer_status=answer_status,
                             question_id=question_id,
                             user_answer=answer_value,
                             user_id=current_user.id,
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
                             lesson_id=lesson_id,
                             lesson_name=lesson_name)
        db.session.add(answer)
        db.session.commit()
        flash("Ответ неверный", "danger")


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы", 'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('index', next=request.url))


class UserView(ModelView):
    column_exclude_list = ('password')


class LessonAdmin(ModelView):
    form_overrides = dict(material=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


class CourseAdmin(ModelView):
    form_overrides = dict(info=CKEditorField, content=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

