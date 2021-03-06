# Python E-learn Shell project

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
3. Создайте файл config.py и задайте в нем переменные:
```
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SECRET_KEY = "YOUR_SECRET_KEY"
SQLALCHEMY_TRACK_MODIFICATIONS = False
CKEDITOR_FILE_UPLOADER = 'upload'
UPLOADED_PATH = os.path.join(basedir, 'uploads')
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
run.py или просто run
```
