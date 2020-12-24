from flask_sqlalchemy import SQLAlchemy

"""
Модель базы данных, включает в себя данные по курсам, урокам, а также таблицу соответствия уроков к курсам
"""

db = SQLAlchemy()

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return 'Курс {} {}'.format(self.course_id, self.name)

class Lessons(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String, nullable=False)
    material_type = db.Column(db.String, nullable=False)
    material = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return 'Урок {} {}'.format(self.lesson_id, self.lesson_name)

class Lessons_To_Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, primary_key=True)