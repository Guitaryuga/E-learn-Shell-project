from webapp.model import db, Courses, Lessons, Lessons_To_Courses

"""
Здесь описана база данных в виде питоновских словарей. Далее идут функции, которые вносят данные в db с помощью get_all_courses. 
"""


courses = [{'course_id': '1', 'name': 'Курс №5'}, 
           {'course_id': '2', 'name': "Курс №5 кпп"},
           {'course_id': '3', 'name': 'Курс №1'}, 
           {'course_id': '4', 'name': 'Курс №2'}]

lessons_1 = [{'lesson_id':'1', 'lesson_name': 'Вступление', 'material_type': 'text', 'material': 'Проявления опасности веществ при их перевозках воздущным транспортом' },
             {'lesson_id': '2', 'lesson_name': 'Введение', 'material_type': 'video', 'material': 'https://www.youtube.com/embed/UBX8MWYel3s'},
             {'lesson_id': '3', 'lesson_name': 'Общие принципы', 'material_type': 'image', 'material': 'https://utv.ru/media/screen_image/a3d190f180f813e507663ab102a239a1800x450.jpg'},
             {'lesson_id': '4', 'lesson_name': 'Правовая основа', 'material_type': 'text', 'material': 'Text_sample'},
             {'lesson_id': '5', 'lesson_name': 'Что представляют собой опансые грузы?', 'material_type': 'text', 'material': 'Text_sample'},
           ]

lessons_to_courses = [{'course_id': '1', 'lesson_id':'1'}, {'course_id': '1', 'lesson_id':'2'}, 
                      {'course_id': '1', 'lesson_id':'3'}, {'course_id': '1', 'lesson_id':'4'},
                      {'course_id': '1', 'lesson_id':'5'}, {'course_id': '2', 'lesson_id': '1'},
                      {'course_id': '2', 'lesson_id': '2'}, {'course_id': '2', 'lesson_id': '3'}]

def extracting_data():
    for check_course in courses:
      course_id = check_course['course_id']
      name = check_course['name']
      save_courses(course_id, name)
    for check_lesson in lessons_1:
      lesson_id = check_lesson['lesson_id']
      lesson_name = check_lesson['lesson_name']
      material_type = check_lesson['material_type']
      material = check_lesson['material']
      save_lessons(lesson_id, lesson_name, material_type, material)
    for check in lessons_to_courses:
      course_id = check['course_id']
      lesson_id = check['lesson_id']
      save_check(course_id, lesson_id)

def save_courses(course_id, name):
  new_courses = Courses(course_id=course_id, name=name)
  db.session.add(new_courses)
  db.session.commit()

def save_lessons(lesson_id, lesson_name, material_type, material):
  new_lessons = Lessons(lesson_id=lesson_id, lesson_name=lesson_name, material_type=material_type, material=material)
  db.session.add(new_lessons)
  db.session.commit()

def save_check(course_id, lesson_id):
  new_check = Lessons_To_Courses(course_id=course_id, lesson_id=lesson_id)
  db.session.add(new_check)
  db.session.commit()

