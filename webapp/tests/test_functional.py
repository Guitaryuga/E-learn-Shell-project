

def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_login_page(test_client):
    response = test_client.get('/users/login')
    assert response.status_code == 200


def test_register_page(test_client):
    response = test_client.get('/users/register')
    assert response.status_code == 200

