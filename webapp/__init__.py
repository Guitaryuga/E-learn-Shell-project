from flask import Flask, render_template, url_for, flash, redirect, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate

from webapp.model import db, Course, Lesson, lessons_to_courses, User 
from webapp.forms import LoginForm, RegistrationForm
from webapp.decorators import admin_required

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

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

    @app.route("/test")  # тестовый роут с тестовой страницей для проверки отображения материала
    def dash():
        course = Course.query.get(1)
        title = course.id
        return render_template('test_template.html')

    @app.route("/admin")
    @admin_required
    def admin_index():
        title = "Панель управления"
        return render_template('admin.html', page_title=title)

    @app.route("/course/<course_id>")
    def course(course_id):
        if current_user.is_authenticated:
            course = Course.query.get(course_id)
            title = course.name
            session['course_id'] = course_id
            return render_template('course.html', page_title=title, course_id=course_id, lesson_list=course.lessons)
        else:
            flash('Вам необходимо зарегистрироваться или войти')
            return redirect(url_for('index'))
        
    @app.route("/lesson/<lesson_id>")
    def lesson(lesson_id):
        lesson = Lesson.query.get(lesson_id)
        course_id = session.get('course_id', None) 
        course = Course.query.get(course_id) 
        title = lesson.lesson_name
        if lesson.material_type == 'text':
            return render_template('text_lesson.html', page_title=title, lesson_title=title, material=lesson.material, lesson_list=course.lessons)
        elif lesson.material_type == 'image':
            return render_template('image_lesson.html', page_title=title, lesson_title=title, material=lesson.material, lesson_list=course.lessons)
        elif lesson.material_type == 'video':
            return render_template('video_lesson.html', page_title=title, lesson_title=title, material=lesson.material, lesson_list=course.lessons)
        elif lesson.material_type == 'pdf':
            return render_template('pdf_lesson.html',  page_title=title, lesson_title=title, material=lesson.material, lesson_list=course.lessons)

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('signin.html', page_title=title, form=login_form) 

    @app.route("/process-login", methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
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

    @app.route("/register")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Регистрация пользователя"
        form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=form)

    @app.route("/process-reg", methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, fio=form.fio.data, 
                            company=form.company.data, position=form.position.data, 
                            date_of_birth=form.date_of_birth.data, phone_number=form.phone_number.data, role='user')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for('register'))
        flash('Пожалуйста, исправьте ошибки в форме')
        return redirect(url_for('register'))

    return app
