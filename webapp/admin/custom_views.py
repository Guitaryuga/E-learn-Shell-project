from flask import request, flash, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
from flask_ckeditor import CKEditorField

"""Спец.вьюшки для отдельных разделов админки"""


class MyAdminIndexView(AdminIndexView):
    """Класс для доступа к админ-панели только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))


class UserView(ModelView):
    """Класс для доступа к учетным записям пользователей только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))

    column_exclude_list = ('password')


class LessonAdmin(ModelView):
    """Класс для доступа к редактированию материала уроков только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))

    """Изменение форм редактирования на формы с подключенным CKEditor"""
    form_overrides = dict(material=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


class CourseAdmin(ModelView):
    """Класс для доступа к редактированию материала курсов только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))

    """Изменение форм редактирования на формы с подключенным CKEditor"""
    form_overrides = dict(info=CKEditorField, content=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


class UserAnswerAdmin(ModelView):
    """Класс для доступа к ответам на вопросы курсов пользователей только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))


class QuestionAdmin(ModelView):
    """Класс для доступа к вопросам в курсах только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))


class AnswerVariantAdmin(ModelView):
    """Класс для доступа к варинатам ответа для формирования тестов только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))


class UploadAdmin(FileAdmin):
    """Класс для доступа странице загрузки файлов только для администраторов"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))


class MainIndexLink(MenuLink):
    "Ссылка на основное приложение в верхней панели админки"
    def get_url(self):
        return url_for("material.index")
