from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate

from webapp.model import db, Course, Lesson, lessons_to_courses, users_to_courses, User
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
        if current_user.is_authenticated:
            course_1 = Course.query.get(1)
            course_2 = Course.query.get(2)
            course_3 = Course.query.get(3)
            course_4 = Course.query.get(4)
            user_courses = current_user.courses
            title = "Список курсов"
            return render_template('index.html', page_title=title, course_1=course_1, course_2=course_2, course_3=course_3, course_4=course_4, user_courses=user_courses)
        else:
            title = "Список курсов"
            return render_template('index.html', page_title=title)


    @app.route("/confirmation", methods=['POST'])  # процесс подтверждения записи на курс
    def process_confirm():
        page_data = request.form.to_dict()
        course_id = page_data['course_id']
        course = Course.query.get(course_id)
        user = current_user
        user.courses.append(course)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно поступили на курс!', 'success')
        return redirect('/')

    @app.route("/test")  # тестовый роут с тестовой страницей для проверки отображения материала
    def test():
        course = current_user
        title = course.id
        test_sample = Course.query.get(1)
        test_sample2 = current_user.courses
        if test_sample in test_sample2:
            test_sample3 = "Confirmed"
        return render_template('test_template.html', test_sample=test_sample, test_sample2=test_sample2, test_sample3=test_sample3)

    @app.route("/test2", methods=['POST']) 
    def process_test():
        print(request.form)
        return redirect('/test')

    @app.route("/admin")
    @admin_required
    def admin_index():
        title = "Панель управления"
        return render_template('admin.html', page_title=title)

    @app.route("/course/<course_id>") #путь к курсам
    def course(course_id):
        if current_user.is_authenticated:
            course = Course.query.get(course_id)
            title = course.name
            session['course_id'] = course_id
            return render_template('course.html', page_title=title, course_id=course_id, lesson_list=course.lessons)
        else:
            flash('Вам необходимо зарегистрироваться или войти', 'danger')
            return redirect(url_for('index'))
        
    @app.route("/lesson/<lesson_id>") # путь к урокам в курсах
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
                flash('Вы вошли на сайт', 'success')
                return redirect(url_for("index"))               
        flash('Неверное имя пользователя или пароль', 'danger')
        return redirect(url_for("login")) 

    @app.route("/user/<username>")
    @login_required
    def user(username):
        profile = User.query.get(current_user.id)
        courses = profile.courses
        title = "Профиль"
        return render_template('profile.html', page_title=title, courses=courses)
        
    @app.route("/logout")
    def logout():
        logout_user()
        flash('Вы вышли из учетной записи', 'success' )
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
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for('register'))
        flash('Пожалуйста, исправьте ошибки в форме', 'danger')
        return redirect(url_for('register'))

    return app
