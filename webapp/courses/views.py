from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from webapp.courses.forms import QuestionForm
from webapp.courses.models import Course, Lesson, Question
from webapp.decorators import check_confirmed
from webapp.user.models import User, User_answer
from webapp.courses.functions import checking_answer, get_redirect_target
from webapp.db import db

blueprint = Blueprint('material', __name__)


"""Роуты и функции, относящиеся к разделу курсов, их содержанию и доступу"""


@blueprint.route("/")
def index():
    """Главная страница"""
    all_courses = Course.query.all()
    title = "Список курсов"
    if current_user.is_authenticated:
        user_courses = current_user.courses
        return render_template('courses/index.html', page_title=title,
                               user_courses=user_courses,
                               all_courses=all_courses)
    else:
        title = "Список курсов"
        return render_template('courses/index.html', page_title=title,
                               all_courses=all_courses)


@blueprint.route("/confirmation", methods=['POST'])
@login_required
@check_confirmed
def process_confirm():
    """Процесс подтверждения записи на курс

    Функция вносит запрашиваемый курс в
    many-to-many таблицу users_to_courses
    """
    page_data = request.form.to_dict()
    course_id = page_data['course_id']
    course = Course.query.get(course_id)
    user = current_user
    user.courses.append(course)
    db.session.add(user)
    db.session.commit()
    flash('Вы успешно поступили на курс!', 'success')
    return redirect(get_redirect_target())


@blueprint.route("/answerchecking/<course_id>/<lesson_id>/<question_id>", methods=['POST'])
def process_test(question_id, lesson_id, course_id):
    """Проверка правильности ВЫБОРА правильного варианта ответа

    Функция собирает данные для проверки правильности
    ответа на вопрос в определенном уроке и курсе и передает их в функцию
    checking_answer.
    """
    try:
        answer_data = request.form.to_dict()
        answer_value = answer_data['answer']
        correct_question = Question.query.get(question_id)
        correct_answer = correct_question.correctanswer
        correct_lesson = Lesson.query.get(lesson_id)
        lesson_id = correct_lesson.id
        lesson_name = correct_lesson.name
        checking_answer(correct_answer, answer_value, question_id,
                        lesson_id, lesson_name, course_id)
        return redirect(get_redirect_target())
    except KeyError:
        flash('Необходимо выбрать вариант ответа', 'danger')
        return redirect(get_redirect_target())


'''
Проверка правильности написанного ответа
'''


@blueprint.route("/handwritechecking/<course_id>/<lesson_id>/<question_id>",
                 methods=['POST'])
def process_writing(question_id, lesson_id, course_id):
    """Проверка правильности ВВЕДЕННОГО ответа

    Функция собирает данные для проверки правильности
    ответа на вопрос в определенном уроке и курсе и передает их в функцию
    checking_answer.
    """
    form = QuestionForm()
    answer_value = form.answer.data
    correct_question = Question.query.get(question_id)
    correct_answer = correct_question.correctanswer
    correct_lesson = Lesson.query.get(lesson_id)
    lesson_id = correct_lesson.id
    lesson_name = correct_lesson.name
    checking_answer(correct_answer, answer_value, question_id,
                    lesson_id, lesson_name, course_id)
    return redirect(get_redirect_target())


@blueprint.route("/course/<course_id>")
@login_required
def course(course_id):
    """Путь в запрашиваемому курсу"""
    course = Course.query.get(course_id)
    user = User.query.get(current_user.id)
    if course in user.courses:
        return render_template('courses/course.html', course=course,
                               course_id=course_id,
                               page_title=course.name, lesson=course,
                               contents=course.content)
    else:
        flash('Сначала Вам нужно записаться на курс!', 'danger')
        return redirect(url_for("material.index"))


@blueprint.route("/course/<course_id>/lesson/<lesson_id>")
@login_required
def lesson(course_id, lesson_id):
    """Путь к запрашиваемым урокам в курсах"""
    form = QuestionForm()
    lesson = Lesson.query.get(lesson_id)
    course = Course.query.get(course_id)
    questions = lesson.questions
    user_answer = User_answer
    user = User.query.get(current_user.id)
    if course in user.courses:
        return render_template('courses/lesson.html', course=course,
                               course_id=course_id, form=form,
                               lesson=lesson, page_title=lesson.name,
                               questions=questions, user_answer=user_answer)
    else:
        flash('Сначала Вам нужно записаться на курс!', 'danger')
        return redirect(url_for("material.index"))
