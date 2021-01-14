from webapp.model import db, Course, Lesson, lessons_to_courses

"""
Здесь описана база данных в виде питоновских словарей. Далее идут функции, которые вносят данные в db с помощью get_all_courses. 
"""


courses = [{'course_id': 1, 'name': 'Курс №5'}, 
           {'course_id': 2, 'name': "Курс №5 кпп"},
           {'course_id': 3, 'name': 'Курс №1'}, 
           {'course_id': 4, 'name': 'Курс №2'}]

lessons_1 = [{'lesson_id': 1, 'lesson_name': 'Вступление', 'material_type': 'text', 'material': 'Проявления опасности веществ при их перевозках воздушным транспортом'},
             {'lesson_id': 2, 'lesson_name': 'Введение', 'material_type': 'video', 'material': 'https://www.youtube.com/embed/UBX8MWYel3s'},
             {'lesson_id': 3, 'lesson_name': 'Общие принципы', 'material_type': 'image', 'material': 'https://utv.ru/media/screen_image/a3d190f180f813e507663ab102a239a1800x450.jpg'},
             {'lesson_id': 4, 'lesson_name': 'Правовая основа', 'material_type': 'text', 'material': 'Text_sample'},
             {'lesson_id': 5, 'lesson_name': 'Что представляют собой опасные грузы?', 'material_type': 'text', 'material': 'Text_sample'},
             {'lesson_id': 6, 'lesson_name': 'Общие принципы классификации опасных грузов', 'material_type': 'pdf', 'material': '/static/pdf/posobie_1.pdf'}
           ]

lessons_to_courses = {1: [1, 2, 3, 4, 5, 6], 
                      2: [1, 2, 3],
                      3: [3, 4],
                      4: [1, 2]}


def extracting_data():
  for check_lesson in lessons_1:
    lesson_id = check_lesson['lesson_id']
    lesson_name = check_lesson['lesson_name']
    material_type = check_lesson['material_type']
    material = check_lesson['material']
    save_lessons(lesson_id, lesson_name, material_type, material)
  
  for check_course in courses:
    course_id = check_course['course_id']
    name = check_course['name']
    save_courses(course_id, name)


def save_courses(id, name):
  courses_exists = Course.query.filter(Course.name == name).count()
  if not courses_exists:
    new_course = Course(id=id, name=name)
    new_course.lessons = [Lesson.query.get(x) for x in lessons_to_courses[id]]
    db.session.add(new_course)
    db.session.commit()


def save_lessons(id, lesson_name, material_type, material):
  lessons_exists = Lesson.query.filter(Lesson.lesson_name == lesson_name).count()
  if not lessons_exists:
    new_lessons = Lesson(id=id, lesson_name=lesson_name, material_type=material_type, material=material)
    db.session.add(new_lessons)
    db.session.commit()
