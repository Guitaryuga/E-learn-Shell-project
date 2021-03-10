import pytest
from webapp.user.models import User, User_answer
from webapp.courses.models import Course, Lesson, Question, AnswerVariant
from webapp.db import db
from webapp import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User(id='1', username='patkennedy79@gmail.com', fio='Patrick Kennedy',
                password='FlaskIsAwesome', company='VIP', position='CEO',
                date_of_birth='20.09.1994', phone_number='+79841502556',
                role='user')
    return user


@pytest.fixture(scope='module')
def new_user_answer():
    user_answer = User_answer(id='1', lesson_id='1', lesson_name='Test lesson',
                              user_answer='Test answer', answer_status='Correct')
    return user_answer


@pytest.fixture(scope='module')
def new_course():
    course = Course(id='1', name='Test course', info='Here will be text',
                    conditions='$$$', content='Contents of course')
    return course


@pytest.fixture(scope='module')
def new_lesson():
    lesson = Lesson(id='1', name='Test lesson', material_type='noslides',
                    material='/static/file3.png', questions_to_pass='2')
    return lesson


@pytest.fixture(scope='module')
def new_question():
    question = Question(id='1', correctanswer='True answer', question_text='Test question',
                        question_type='closed')
    return question

@pytest.fixture(scope='module')
def new_answervariant():
    answervariant = AnswerVariant(id='1', answer_text='test answer')
    return answervariant


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['LOGIN_DISABLED'] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
            course1 = Course(id='1', name='Test', info='Info', conditions='$$$', content='Content')
            db.session.add(course1)
            db.session.commit()
            yield testing_client  # this is where the testing happens!
