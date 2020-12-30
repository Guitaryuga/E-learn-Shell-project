from flask import Flask, render_template, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user

from webapp.database import courses, lessons_1
from webapp.model import db, Course, Lesson, lessons_to_courses #User #в плане использовать данные непосредственно из БД
from webapp.forms import LoginForm

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = "Список курсов"
        return render_template('index.html', page_title=title)

    @app.route("/course/<course_id>")
    def course(course_id):
        for check_id in courses:
            if check_id['course_id'] == course_id:
                title = check_id['name']
                lesson_list = lessons_1
        return render_template('course.html', title = title, course_id= course_id, lesson_list = lesson_list)
    
    @app.route("/lesson/<lesson_id>")
    def lesson(lesson_id):
        lesson_list = lessons_1
        for check_lesson in lessons_1:
            if check_lesson['lesson_id'] == lesson_id:
                title = check_lesson['lesson_name']
                material = check_lesson['material']
                if check_lesson['material_type'] == 'video':
                    return render_template('video_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list) # проба использования разных типов материалов
                elif check_lesson['material_type'] == 'image':
                    return render_template('image_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list)
                else:
                    return render_template('text_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list) 

    @app.route("/login")
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('signin.html', page_title = title, form= login_form) 

    @app.route("/process-login", methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for("index"))
                
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for("login"))    
     
    @app.route("/logout")
    def logout():
        logout_user()
        flash('Вы вышли из учетной записи')
        return redirect(url_for("index"))
    
    return app