import pytest
from webapp.user.models import User, User_answer
from webapp.courses.models import Course, Lesson, Question, AnswerVariant
from webapp.db import db
from webapp import create_app
from webapp.database import extracting_data


@pytest.fixture
def test_client(scope='module'):
    flask_app = create_app()
    flask_app.config['LOGIN_DISABLED'] = False
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    flask_app.config['BCRYPT_LOG_ROUNDS'] = 4
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            testing_client.post('users/process-reg',
                                data=dict(username='test@example.com',
                                          fio='Test testing',
                                          password='example123',
                                          password2='example123',
                                          company='T.E.S.T',
                                          position='Manager',
                                          date_of_birth='10.01.1984',
                                          phone_number='+70000000000',
                                          role='user'))
            extracting_data()
            yield testing_client  # this is where the testing happens!


@pytest.fixture
def login(test_client):
    return test_client.post('users/process-login',
                            data=dict(username='test@example.com',
                                      password='example123'),
                            follow_redirects=True)


@pytest.fixture
def confirmation(test_client):
    return test_client.post('/confirmation', data=dict(course_id=1),
                            follow_redirects=True)


@pytest.fixture
def answerchecking(test_client):
    return test_client.post('/answerchecking/1/1/1',
                            data=dict(answer='This thing'),
                            follow_redirects=True)


@pytest.fixture
def wrong_answerchecking(test_client):
    return test_client.post('/answerchecking/1/1/1',
                            data=dict(answer='That thing'),
                            follow_redirects=True)


@pytest.fixture
def handwritechecking(test_client):
    return test_client.post('/handwritechecking/1/1/2',
                            data=dict(answer='Test'),
                            follow_redirects=True)


@pytest.fixture
def wrong_handwritechecking(test_client):
    return test_client.post('/handwritechecking/1/1/2',
                            data=dict(answer='NotTest'),
                            follow_redirects=True)


@pytest.fixture(scope='module')
def new_user():
    user = User(id='1', username='patkennedy79@gmail.com',
                fio='Patrick Kennedy', password='FlaskIsAwesome',
                company='VIP', position='CEO',
                date_of_birth='20.09.1994', phone_number='+79841502556',
                role='user')
    return user


@pytest.fixture(scope='module')
def new_user_answer():
    user_answer = User_answer(id='1', lesson_id='1',
                              lesson_name='Test lesson',
                              user_answer='Test answer',
                              answer_status='Correct')
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
    question = Question(id='1', correctanswer='True answer',
                        question_text='Test question', question_type='closed')
    return question


@pytest.fixture(scope='module')
def new_answervariant():
    answervariant = AnswerVariant(id='1', answer_text='test answer')
    return answervariant
