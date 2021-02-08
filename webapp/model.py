from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user


from werkzeug.security import generate_password_hash, check_password_hash

"""
Модель базы данных, включает в себя данные по курсам, урокам, а также таблицу соответствия уроков к курсам
"""

db = SQLAlchemy()

lessons_to_courses = db.Table('lessons_to_courses',                       
    db.Column('course_id', db.Integer, db.ForeignKey('Course.id')),        
    db.Column('lesson_id', db.Integer, db.ForeignKey('Lesson.id')),
    db.Column('order', db.Integer))

users_to_courses = db.Table('users_to_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('Course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')))

questions_to_lessons = db.Table('questions_to_lessons', 
    db.Column('lesson_id', db.Integer, db.ForeignKey('Lesson.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('Question.id')))

answervariants_to_questions = db.Table('answervariants_to_questions',
    db.Column('question_id', db.Integer, db.ForeignKey('Question.id')),
    db.Column('answervariant_id', db.Integer, db.ForeignKey('AnswerVariant.id')))
    

class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lessons = db.relationship("Lesson", secondary=lessons_to_courses)
    info = db.Column(db.Text, nullable=True)
    conditions = db.Column(db.String(64))
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Курс {self.id} {self.name}'


class Lesson(db.Model):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    material_type = db.Column(db.String, nullable=False)    
    material = db.Column(db.Text, nullable=True)
    questions = db.relationship("Question", secondary=questions_to_lessons)
    questions_to_pass = db.Column(db.Integer)

    def __repr__(self):
        return f'Урок {self.id} {self.name}'


class Slide(db.Model):
    __tablename__ = 'Slide'
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('Lesson.id', ondelete='CASCADE'), index=True)
    lessons = db.relationship('Lesson', backref='slides')
    link = db.Column(db.String(128))

    def __repr__(self):
        return f'Слайд {self.id} {self.link}'


class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    correctanswer = db.Column(db.String(128))
    question_text = db.Column(db.String(128))
    question_type = db.Column(db.String(50))
    answervariants = db.relationship("AnswerVariant", secondary=answervariants_to_questions)
    

    def __repr__(self):
        return f'Вопрос {self.id} {self.question_text}'


class AnswerVariant(db.Model):
    __tablename__ = 'AnswerVariant'
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String(128))

    def __repr__(self):
        return f'Ответ {self.id} {self.answer_text}'


class User_answer(db.Model):
    __tablename__ = 'User_answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'), index=True) #test
    users = db.relationship('User', backref='user_answers') #test
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id', ondelete='CASCADE'), index=True) #test
    questions = db.relationship('Question', backref='user_answers') #test
    user_answer = db.Column(db.String(50))
    answer_status = db.Column(db.String(50))

    def __repr__(self):
        return f'Пользователь {self.id} {self.user_answer}'


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
