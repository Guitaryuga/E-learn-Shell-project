def test_confirmation(test_client, login, confirmation):
    """
    Тест процесса записи на курс: стоит защита от подмены
    ссылки на редирект, категория появляющего алерта - success
    """
    login
    confirmation
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Index page' in response.data


def test_confirmation_without_login(test_client, confirmation):
    """
    Тест процесса записи на курс БЕЗ авторизации, должен
    быть редирект на главную, категория алерта - danger
    """
    response = confirmation
    assert response.status_code == 200
    assert b'Sign in' in response.data
    assert b'danger' in response.data


def test_confirmed_course_and_lesson(test_client, login, confirmation):
    """
    Тест на доступ к курсу и уроку после логина и записи
    """
    login
    confirmation
    course = test_client.get('/course/1', follow_redirects=True)
    assert course.status_code == 200
    assert b'Main course' in course.data

    lesson = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert lesson.status_code == 200
    assert b'Main course' in lesson.data
    assert b'Test question' in lesson.data


def test_course_and_lesson_without_confirmation(test_client, login):
    """
    Тест доступа к курсу и урокам после логина но БЕЗ записи
    """
    login
    course = test_client.get('/course/1', follow_redirects=True)
    assert course.status_code == 200
    assert b'Index page' in course.data
    assert b'danger' in course.data

    lesson = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert lesson.status_code == 200
    assert b'Index page' in lesson.data
    assert b'danger' in lesson.data


def test_course_and_lesson_without_auth(test_client):
    """
    Тест доступа к курсу и урокам БЕЗ авторизации, должен
    быть редирект на страницу логина, категория алерта - danger
    """
    course = test_client.get('/course/1', follow_redirects=True)
    assert course.status_code == 200
    assert b'danger' in course.data
    assert b'Sign in' in course.data

    lesson = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert lesson.status_code == 200
    assert b'danger' in lesson.data
    assert b'Sign in' in lesson.data


def test_not_confirmed_another_course_and_lesson(test_client, login,
                                                 confirmation):
    """
    Тест доступа к курсу и уроку в этом курсе, на который пользователь
    не записывался, но авторизован, должен быть редирект на главную
    страницу, категория алерта - danger
    """
    login
    confirmation
    course = test_client.get('/course/2', follow_redirects=True)
    assert course.status_code == 200
    assert b'Index page' in course.data
    assert b'danger' in course.data

    lesson = test_client.get('/course/2/lesson/2', follow_redirects=True)
    assert lesson.status_code == 200
    assert b'Index page' in lesson.data
    assert b'danger' in lesson.data


def test_different_lessons(test_client, login, confirmation):
    """
    Тест доступа к разным урокам и различным типам материала в них
    """
    login
    confirmation
    lesson_1 = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert lesson_1.status_code == 200
    assert b'Main course' in lesson_1.data
    assert b'Test question' in lesson_1.data
    assert b'This thing' in lesson_1.data
    assert b'Here will be your text material' in lesson_1.data

    lesson_2 = test_client.get('/course/1/lesson/2', follow_redirects=True)
    assert lesson_2.status_code == 200
    assert b'Main course' in lesson_2.data
    assert b'docs.google.com' in lesson_2.data
    assert b'Test question #2' in lesson_2.data

    lesson_3 = test_client.get('/course/1/lesson/3', follow_redirects=True)
    assert lesson_3.status_code == 200
    assert b'Main course' in lesson_3.data
    assert b'img src="/static/slides/1.jpg"' in lesson_3.data
    assert b'Test question #3' in lesson_3.data
    assert b'Yes' in lesson_3.data

    lesson_4 = test_client.get('/course/1/lesson/4', follow_redirects=True)
    assert lesson_4.status_code == 200
    assert b'Main course' in lesson_4.data
    assert b'YouTube video' in lesson_4.data
    assert b'Test question #4' in lesson_4.data
    assert b'Answer!' in lesson_4.data

    lesson_5 = test_client.get('/course/1/lesson/5', follow_redirects=True)
    assert lesson_5.status_code == 200
    assert b'Main course' in lesson_5.data
    assert b'<iframe src="/static/pdf/dummy.pdf"' in lesson_5.data
    assert b'Test question #5' in lesson_5.data
    assert b'Testing' in lesson_5.data

    lesson_6 = test_client.get('/course/1/lesson/6', follow_redirects=True)
    assert lesson_6.status_code == 200
    assert b'Main course' in lesson_6.data
    assert b'Text_sample' in lesson_6.data
    assert b'Test question #6'
