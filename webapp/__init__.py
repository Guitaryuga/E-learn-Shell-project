from flask import Flask, flash, redirect, render_template, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate

from webapp.model import db, Course, Lesson, lessons_to_courses, Question, User, users_to_courses, User_answer, Answer
from webapp.forms import LoginForm, QuestionForm, RegistrationForm, UserForm
from webapp.decorators import admin_required
from webapp.functions import checking_answer, get_redirect_target, MyAdminIndexView, UserView


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Course, db.session))
    admin.add_view(ModelView(Lesson, db.session))
    admin.add_view(ModelView(User_answer, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Answer, db.session))

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        all_courses = Course.query.all()
        title = "Список курсов"
        if current_user.is_authenticated:
            user_courses = current_user.courses
            return render_template('index.html', page_title=title, user_courses=user_courses, all_courses=all_courses)
        else:
            title = "Список курсов"
            return render_template('index.html', page_title=title, all_courses=all_courses)
            

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
        test_sample = User.query.filter(User.fio == 'Поляков Петр').all()
        test_sample2 = [1, 2, 3]
        test_sample3 = 1
        if test_sample3 in test_sample2:
            test_sample4 = 'correct'
        else:
            test_sample4 = 'wrong'
        return render_template('test_template.html', test_sample=test_sample, test_sample2=test_sample2, test_sample3=test_sample3, test_sample4=test_sample4)

    @app.route("/answerchecking/<question_id>", methods=['POST'])  # проверка правильности выбора правильного варианта ответа
    def process_test(question_id):
        try:
            answer_data = request.form.to_dict()
            answer_value = answer_data['answer']
            correct_question = Question.query.get(question_id)
            correct_answer = correct_question.correctanswer
            checking_answer(correct_answer, answer_value, question_id)
            return redirect(get_redirect_target())
        except KeyError:
            flash('Необходимо выбрать вариант ответа', 'danger')
            return redirect(get_redirect_target())

    @app.route("/handwritechecking/<question_id>", methods=['POST'])  # проверка правильности написанного ответа
    def process_writing(question_id):
        form = QuestionForm()
        answer_value = form.answer.data
        correct_question = Question.query.get(question_id)
        correct_answer = correct_question.correctanswer
        checking_answer(correct_answer, answer_value, question_id)
        return redirect(get_redirect_target())


    @app.route("/course/<course_id>") #путь к курсам
    def course(course_id):
        if current_user.is_authenticated:
            course = Course.query.get(course_id)
            return render_template('course.html', course=course, course_id=course_id, page_title=course.name, lesson=lesson) # lesson=lesson - заглушка, course/<course_id> должен выдавать
        else:                                                                                                                 # кртакое содержание или инфу по курсу, "Содержание" сделать кликабельным
            flash('Вам необходимо зарегистрироваться или войти', 'danger')
            return redirect(url_for('index'))
        
    @app.route("/course/<course_id>/lesson/<lesson_id>") # путь к урокам в курсах
    def lesson(course_id, lesson_id):
        form = QuestionForm()
        lesson = Lesson.query.get(lesson_id)
        course = Course.query.get(course_id)
        question = Question.query.get(lesson_id)
        checked = User_answer.query.filter(User_answer.user_id == current_user.id, User_answer.question_id == question.id).all()
        return render_template('lesson.html', checked=checked, course=course, course_id=course_id, form=form, lesson=lesson, page_title=lesson.lesson_name, question=question)

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('signin.html', form=login_form, page_title=title) 

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
        user_progress = User_answer.query.filter(User_answer.user_id == current_user.id).all()
        answered_questions = []
        for lessons in user_progress:
            answered_questions.append(lessons.question_id)
        title = "Профиль"
        return render_template('profile.html', answered_questions=answered_questions, courses=courses, page_title=title, user_progress=user_progress)
        
    @app.route("/logout")
    def logout():
        logout_user()
        flash('Вы вышли из учетной записи', 'success')
        return redirect(url_for("index"))

    @app.route("/register")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Регистрация пользователя"
        form = RegistrationForm()
        return render_template('registration.html', form=form, page_title=title)

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

    # @app.route("/admin", methods=['GET', 'POST']) # попытка сделать небольшую админку, чтобы можно было как-то отслеживать пользователей
    # @admin_required
    # def admin_index():
    #     title = "Панель управления"
    #     form = UserForm()
    #     user = form.user_name.data
    #     profiles = User.query.all()
    #     try:
    #         if user:
    #             correct_user = User.query.filter(User.fio == user).all()
    #             for info in correct_user:
    #                 user_id = info.id
    #             particular_user = User.query.get(user_id)
    #             courses = particular_user.courses
    #             user_progress = User_answer.query.filter(User_answer.user_id == user_id).all()
    #             answered_questions = []
    #             for lessons in user_progress:
    #                 answered_questions.append(lessons.question_id)
    #             return render_template('admin.html', page_title=title, profiles=profiles, form=form, 
    #                                     answered_questions=answered_questions, courses=courses, user_progress=user_progress, user=user)
    #     except UnboundLocalError:
    #         flash('Неверный формат данных', 'danger')
    #         return redirect(get_redirect_target())
    #     return render_template('admin.html', page_title=title, profiles=profiles, form=form)

    return app
