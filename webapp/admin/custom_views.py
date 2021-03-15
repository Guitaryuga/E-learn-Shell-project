from flask import request, flash, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_ckeditor import CKEditorField

'''
Спец.вьюшки для отдельных разделов админки
'''


class MyAdminIndexView(AdminIndexView):
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
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))

    form_overrides = dict(material=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


class CourseAdmin(ModelView):
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))

    form_overrides = dict(info=CKEditorField, content=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


class UserAnswerAdmin(ModelView):
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
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("У вас недостаточно прав для просмотра этой страницы",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас недостаточно прав для просмотра этой страницы", 'danger')
        return redirect(url_for('material.index', next=request.url))
