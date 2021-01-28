from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

"""
Модель базы данных, включает в себя данные по курсам, урокам, а также таблицу соответствия уроков к курсам
"""

db = SQLAlchemy()


lessons_to_courses = db.Table('lessons_to_courses',                       
    db.Column('course_id', db.Integer, db.ForeignKey('Course.id')),        
    db.Column('lesson_id', db.Integer, db.ForeignKey('Lesson.id')))

users_to_courses = db.Table('users_to_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('Course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')))


class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lessons = db.relationship("Lesson", secondary=lessons_to_courses)

    def __repr__(self):
        return f'Курс {self.id} {self.name}'


class Lesson(db.Model):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String, nullable=False)
    material_type = db.Column(db.String, nullable=False)
    material = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Урок {self.id} {self.lesson_name}'

      
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
