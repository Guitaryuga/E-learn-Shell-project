from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    answer = StringField('Ответ', validators=[DataRequired()],
                         render_kw={"class": "form-control",
                         "placeholder": "Ваш ответ"})
    submit = SubmitField('Ответить',
                         render_kw={"class": "btn btn-primary mt-2"})
