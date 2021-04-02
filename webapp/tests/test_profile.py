def test_profile(test_client, login):
    """
    Тест доступности профиля с авторизованным пользователем
    """
    login
    response = test_client.get('users/profile/test@example.com')
    assert response.status_code == 200
    assert b'Profile page' in response.data
    assert b'E-mail' in response.data


def test_profile_without_auth(test_client):
    """
    Тест доступности профиля БЕЗ авторизации, должен
    быть редирект на страницу логина
    """
    response = test_client.get('users/profile/test@example.com',
                               follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign in' in response.data
