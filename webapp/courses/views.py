from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from webapp.courses.forms import QuestionForm
from webapp.courses.models import Course, Lesson, Question
from webapp.user.models import User, User_answer
from webapp.courses.functions import checking_answer, get_redirect_target
from webapp.db import db

blueprint = Blueprint('material', __name__)


@blueprint.route("/")
def index():
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


'''
Процесс подтверждения записи на курс
'''


@blueprint.route("/confirmation", methods=['POST'])
@login_required
def process_confirm():
    page_data = request.form.to_dict()
    course_id = page_data['course_id']
    course = Course.query.get(course_id)
    user = current_user
    user.courses.append(course)
    db.session.add(user)
    db.session.commit()
    flash('Вы успешно поступили на курс!', 'success')
    # return redirect(url_for('material.index'))
    return redirect(get_redirect_target())


'''
Проверка правильности выбора правильного варианта ответа
'''


@blueprint.route("/answerchecking/<lesson_id>/<question_id>", methods=['POST'])
def process_test(question_id, lesson_id):
    try:
        answer_data = request.form.to_dict()
        answer_value = answer_data['answer']
        correct_question = Question.query.get(question_id)
        correct_answer = correct_question.correctanswer
        correct_lesson = Lesson.query.get(lesson_id)
        lesson_id = correct_lesson.id
        lesson_name = correct_lesson.name
        checking_answer(correct_answer, answer_value, question_id,
                        lesson_id, lesson_name)
        return redirect(get_redirect_target())
    except KeyError:
        flash('Необходимо выбрать вариант ответа', 'danger')
        return redirect(get_redirect_target())


'''
Проверка правильности написанного ответа
'''


@blueprint.route("/handwritechecking/<lesson_id>/<question_id>",
                 methods=['POST'])
def process_writing(question_id, lesson_id):
    form = QuestionForm()
    answer_value = form.answer.data
    correct_question = Question.query.get(question_id)
    correct_answer = correct_question.correctanswer
    correct_lesson = Lesson.query.get(lesson_id)
    lesson_id = correct_lesson.id
    lesson_name = correct_lesson.name
    checking_answer(correct_answer, answer_value, question_id,
                    lesson_id, lesson_name)
    return redirect(get_redirect_target())


'''
Путь к курсам
'''


@blueprint.route("/course/<course_id>")
@login_required
def course(course_id):
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


'''
Путь к урокам в курсах
'''


@blueprint.route("/course/<course_id>/lesson/<lesson_id>")
@login_required
def lesson(course_id, lesson_id):
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
