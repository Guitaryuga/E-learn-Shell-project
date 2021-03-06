from flask_login import UserMixin, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db

users_to_courses = db.Table('users_to_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('Course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fio = db.Column(db.String(128))
    password = db.Column(db.String(128))
    company = db.Column(db.String(128))
    position = db.Column(db.String(128))
    date_of_birth = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    role = db.Column(db.String(10), index=True)
    courses = db.relationship("Course", secondary=users_to_courses)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class User_answer(db.Model):
    __tablename__ = 'User_answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id',
                                                  ondelete='CASCADE'),
                        index=True)
    users = db.relationship('User', backref='user_answers')
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id',
                                                      ondelete='CASCADE'),
                            index=True)
    questions = db.relationship('Question', backref='user_answers')
    lesson_id = db.Column(db.Integer)
    lesson_name = db.Column(db.String(128))
    user_answer = db.Column(db.String(50))
    answer_status = db.Column(db.String(50))

    def __repr__(self):
        return f'Пользователь {self.user_id}, вопрос {self.question_id}, ответ {self.user_answer}'
