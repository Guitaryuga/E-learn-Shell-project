def test_answer(test_client, login, confirmation, answerchecking):
    """
    Тест процесса проверки выбора правильного варианта ответа в тестовом
    вопросе закрытого типа, категория алерта - success, возможность
    повторно ответить блокируется
    """
    login
    confirmation
    answerchecking
    response = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'list-group-item disabled' in response.data


def test_wrong_answer(test_client, login, confirmation, wrong_answerchecking):
    """
    Тест процесса проверки выбора неправильного варианта ответа в тестовом
    вопросе закрытого типа, категория алерта - danger, возможность повторно
    овтетить остается
    """
    login
    confirmation
    wrong_answerchecking
    response = test_client.get('/course/1/lesson/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'danger' in response.data
    assert b'list-group-item' in response.data


def test_handwriteanswer(test_client, login, confirmation, handwritechecking):
    """
    Тест процесса проверки написанного ПРАВИЛЬНОГО варианта ответа в вопросе
    открытого типа, категория алерта - success, форма овтета блокируется

    """
    login
    confirmation
    handwritechecking
    response = test_client.get('/course/1/lesson/2', follow_redirects=True)
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'form-control' in response.data


def test_wrong_handwriteanswer(test_client, login, confirmation,
                               wrong_handwritechecking):
    """
    Тест процесса проверки написанного НЕПРАВИЛЬНОГО варианта ответа в вопросе
    открытого типа, категория алерта - danger, форма ответа не блокируется
    """
    login
    confirmation
    wrong_handwritechecking
    response = test_client.get('/course/1/lesson/2', follow_redirects=True)
    assert response.status_code == 200
    assert b'danger' in response.data
