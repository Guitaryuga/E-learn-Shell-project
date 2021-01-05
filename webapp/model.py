from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""
Модель базы данных, включает в себя данные по курсам, урокам, а также таблицу соответствия уроков к курсам
"""

db = SQLAlchemy()
Base = declarative_base() # без указания Base выдает ошибку 

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Курс {self.id} {self.name}'

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String, nullable=False)
    material_type = db.Column(db.String, nullable=False)
    material = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Урок {self.id} {self.lesson_name}'

association_table = db.Table('lessons_to_courses', Base.metadata,  #не совсем уверен в использовании db.,
    db.Column('course_id', db.Integer,db.ForeignKey('Course.id')),  #так как без него линтер подчеркивает все красным
    db.Column('lesson_id', db.Integer, db.ForeignKey('Lesson.id'))   #возможно стоит использовать больше импортов
    )

class Parent(Base):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Child", secondary=association_table)

class Child(Base):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)

# class Lessons_To_Courses(db.Model):
#     course_id = db.Column(db.Integer, primary_key=True) # не Primary_key, a foreign_key
#     lesson_id = db.Column(db.Integer, primary_key=True)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     password = db.Column(db.String(128))
#     role = db.Column(db.String(10), index=True)

#     def set_password(self, password):
#         self.password = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password, password)

#     def __repr__(self):
#         return '<User {}>'.format(self.username)