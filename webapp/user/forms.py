from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.user.models import User

'''
Формы для логина и регистрации пользователей
'''


class LoginForm(FlaskForm):
    username = StringField('Логин или e-mail',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Логин или e-mail"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня',
                               default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Войти',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('E-mail',
                           validators=[DataRequired(), Email()],
                           render_kw={"class": "form-control"})
    fio = StringField('Ваше имя',
                      validators=[DataRequired()],
                      render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    company = StringField('Организация',
                          validators=[DataRequired()],
                          render_kw={"class": "form-control"})
    position = StringField('Должность',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    date_of_birth = StringField('Дата рождения(ДД.ММ.ГГГГ)',
                                validators=[DataRequired()],
                                render_kw={"class": "form-control"})
    phone_number = StringField('Номер телефона',
                               validators=[DataRequired()],
                               render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')

    def validate_fio(self, fio):
        users_count = User.query.filter_by(fio=fio.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')
