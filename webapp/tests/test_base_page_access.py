def test_home_page(test_client):
    """
    Тест доступности главной страницы
    без авторизации
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Index page' in response.data


def test_login_page(test_client):
    """
    Тест доступности страницы логина
    """
    response = test_client.get('/users/login')
    assert response.status_code == 200
    assert b'Sign in' in response.data


def test_login_page_with_auth(test_client, login):
    """
    Тест доступности страницы логина
    авторизованному пользователю: должен
    быть редирект на Index page
    """
    login
    response = test_client.get('/users/login', follow_redirects=True)
    assert response.status_code == 200
    assert b'Index page' in response.data


def test_register_page(test_client):
    """
    Тест доступности страницы регистрации
    """
    response = test_client.get('/users/register')
    assert response.status_code == 200
    assert b'Sign up' in response.data


def test_register_page_with_auth(test_client, login):
    """
    Тест доступности страницы регистрации
    акторизованному пользователю: должен быть редирект
    на Index page
    """
    login
    response = test_client.get('/users/register', follow_redirects=True)
    assert response.status_code == 200
    assert b'Index page' in response.data
