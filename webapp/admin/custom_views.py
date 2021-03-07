from flask import request, flash, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
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
