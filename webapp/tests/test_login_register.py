def test_login_process(test_client, login):
    """
    Тест процесса авторизации: должен быть редирект
    на Index page, категория алерта - success
    """
    response = login
    assert response.status_code == 200
    assert b'Index page' in response.data
    assert b'success' in response.data


def test_login_invalid_data(test_client):
    """
    Тест процесса логина с 3 вариантами неправильных данных:
    неправильный логин, неправильный пароль, неправильный логин И
    пароль;во всех случаях должен возвращаться редирект
    на Sign in страницу, категория алерта - 'danger'
    """
    invalid_username = test_client.post('users/process-login',
                                        data=dict(username='123@example.com',
                                                  password='example123'),
                                        follow_redirects=True)
    assert invalid_username.status_code == 200
    assert b'Sign in' in invalid_username.data
    assert b'danger' in invalid_username.data

    invalid_password = test_client.post('users/process-login',
                                        data=dict(username='test@example.com',
                                                  password='example'),
                                        follow_redirects=True)
    assert invalid_password.status_code == 200
    assert b'Sign in' in invalid_password.data
    assert b'danger' in invalid_password.data

    invalid_username_and_password = test_client.post('users/process-login',
                                                     data=dict(username='123@example.com',
                                                               password='example'),
                                                     follow_redirects=True)
    assert invalid_username_and_password.status_code == 200
    assert b'Sign in' in invalid_username_and_password.data
    assert b'danger' in invalid_username_and_password.data


def test_logout(test_client, login):
    """
    Тест процесса выхода из учетной записи:
    должен быть редирект на Index page,
    категория алерта - success
    """
    login
    response = test_client.get('users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Index page' in response.data
    assert b'success' in response.data


def test_logout_without_auth(test_client):
    """
    Тест процесса выхода из учетной записи
    БЕЗ авторизованного пользователя, должен быть редирект
    на Index page, категория алерта - danger
    """
    response = test_client.get('users/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Index page' in response.data
    assert b'danger' in response.data


def test_reg_process(test_client):
    """
    Тест процесса регистрации, если успешно - должен быть редирект на страницу
    логина, категория алерта - success
    """
    response = test_client.post('users/process-reg',
                                data=dict(username='anothertest@example.com',
                                          fio='Test testing test',
                                          password='example123',
                                          password2='example123',
                                          company='T.E.S.T',
                                          position='Manager',
                                          date_of_birth='10.01.1984',
                                          phone_number='+70000000000',
                                          role='user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign in' in response.data
    assert b'success' in response.data


def test_reg_process_invalid_email(test_client):
    """
    Тест процесса регистрации, с ошибкой в поле E-mail:
    использован e-mail уже существующего аккаунта, должен
    быть повторный редирект на страницу регистрации,
    категрия алерта - danger
    """
    response = test_client.post('users/process-reg',
                                data=dict(username='test@example.com',
                                          fio='Test testing test',
                                          password='example123',
                                          password2='example123',
                                          company='T.E.S.T',
                                          position='Manager',
                                          date_of_birth='10.01.1984',
                                          phone_number='+70000000000',
                                          role='user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign up' in response.data
    assert b'danger' in response.data


def test_reg_process_invalid_fio(test_client):
    """
    Тест процесса регистрации, с ошибкой в поле Ф.И.О:
    использовано ФИО уже существующего аккаунта, должен
    быть повторный редирект на страницу регистрации,
    категрия алерта - danger
    """
    response = test_client.post('users/process-reg',
                                data=dict(username='anothertest@example.com',
                                          fio='Test testing',
                                          password='example123',
                                          password2='example123',
                                          company='T.E.S.T',
                                          position='Manager',
                                          date_of_birth='10.01.1984',
                                          phone_number='+70000000000',
                                          role='user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign up' in response.data
    assert b'danger' in response.data


def test_reg_missing_data(test_client):
    """
    Тест процесса регистрации, с несколькими незаполненными полями:
    должен быть повторный редирект на страницу регистрации,
    категрия алерта - danger
    """
    response = test_client.post('users/process-reg',
                                data=dict(username='anothertest@example.com',
                                          fio='Test testing test',
                                          password='example123',
                                          company='T.E.S.T',
                                          phone_number='+70000000000',
                                          role='user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign up' in response.data
    assert b'danger' in response.data
