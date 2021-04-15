def test_new_user(new_user):
    assert new_user.id == '1'
    assert new_user.username == 'patkennedy79@gmail.com'
    assert new_user.fio == 'Patrick Kennedy'
    assert new_user.check_password != 'FlaskIsAwesome'
    assert new_user.company == 'VIP'
    assert new_user.position == 'CEO'
    assert new_user.date_of_birth == '20.09.1994'
    assert new_user.phone_number == '+79841502556'
    assert new_user.role == 'user'
    assert new_user.confirmed == 1
    assert new_user.is_authenticated


def test_user_answer(new_user_answer):
    assert new_user_answer.id == '1'
    assert new_user_answer.lesson_id == '1'
    assert new_user_answer.lesson_name == 'Test lesson'
    assert new_user_answer.user_answer == 'Test answer'
    assert new_user_answer.answer_status == 'Correct'
    assert new_user_answer.answer_status != 'Wrong'


def test_course(new_course):
    assert new_course.id == '1'
    assert new_course.name == 'Test course'
    assert new_course.info == 'Here will be text'
    assert new_course.conditions == '$$$'
    assert new_course.content == 'Contents of course'


def test_lesson(new_lesson):
    assert new_lesson.id == '1'
    assert new_lesson.name == 'Test lesson'
    assert new_lesson.material_type == 'noslides'
    assert new_lesson.material == '/static/file3.png'
    assert new_lesson.questions_to_pass == '2'


def test_question(new_question):
    assert new_question.id == '1'
    assert new_question.correctanswer == 'True answer'
    assert new_question.question_text == 'Test question'
    assert new_question.question_type == 'closed'


def test_answervariant(new_answervariant):
    assert new_answervariant.id == '1'
    assert new_answervariant.answer_text == 'test answer'
