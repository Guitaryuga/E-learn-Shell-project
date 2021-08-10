# Python E-learn Shell project ![Build Status](https://github.com/Guitaryuga/E-learn-Shell-project/actions/workflows/CI.yml/badge.svg)
### Описание
Данный проект представляет собой веб-приложение на flask, которое можно использовать в качестве онлайн-учебника, наполняемого своим материалом.
Все материалы, связанные одной темой, объединяются в курс, который вы разбиваете на уроки и заполняете необходимым вам материалом(текст, презентация, изображения, видео). В конце каждого урока присутствует тестовый вопрос открытого или закрытого типа, который помогает закрепить материал, а также является индикатором, по которому отслеживается индивидуальный прогресс пользователя.
![screenshotforreadme](https://user-images.githubusercontent.com/74609399/108261413-ac8d0480-7174-11eb-829e-0603b622a03b.png)
![screenshotforreadme2](https://user-images.githubusercontent.com/74609399/108261494-c62e4c00-7174-11eb-88c2-ae68776bee5d.png)

### Установка
Для того, чтобы ознакомиться с функционалом и рассмотреть предложенные примеры:

1.Клонируйте репозиторий:
```
git clone https://github.com/Guitaryuga/E-learn-Shell-project.git
```
2. Создайте и активируйте виртуальное окружение, затем установите зависимости:
```
pip install -r requirements.txt
```
3. Задайте переменные окружения в .env:
```
SECRET_KEY="YOUR_VERY_SECRET_KEY_TELL_NOONE"
SQLALCHEMY_DATABASE_URI="Path to you DB"
SECURITY_PASSWORD_SALT="YOUR_SALT"

Если необходима работа модуля Flask-Mail, то также задайте:
MAIL_SERVER=your_mail_server
MAIL_PORT=your_mail_port
MAIL_USE_TLS=1
MAIL_USERNAME=your_mail_username
MAIL_PASSWORD=your_mail_password_or_google_app_password
ADMINS=['your_email_adress']
```
### Создание и наполнение базы данных
Выполните в консоли:
```
create_db.py
```
Затем:
```
get_all_courses.py
```
После этого выполните команду, чтобы создать пользователя с ролью администратора для последующей работы
```
create_admin.py
```
### Запуск
Чтобы локально запустить веб-приложение, выполните в консоли
```
run
```
