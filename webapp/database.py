from webapp.model import db, Course, Lesson, Question, AnswerVariant, lessons_to_courses, Slide


"""
Здесь описана база данных в виде питоновских словарей. Далее идут функции, которые вносят данные в db с помощью get_all_courses. 
"""


courses = [{'course_id': 1, 'name': 'Курс №5'}, 
           {'course_id': 2, 'name': "Курс №5 кпп"},
           {'course_id': 3, 'name': 'Курс №1'}, 
           {'course_id': 4, 'name': 'Курс №2'}]

lessons_1 = [{'lesson_id': 1, 'name': 'Вступление', 'material_type': 'noslides', 'material': 'Проявления опасности веществ при их перевозках воздушным транспортом'},
             {'lesson_id': 2, 'name': 'Введение', 'material_type': 'noslides', 'material': 'https://www.youtube.com/embed/UBX8MWYel3s'},
             {'lesson_id': 3, 'name': 'Общие принципы', 'material_type': 'slides', 'material': 'slides'},
             {'lesson_id': 4, 'name': 'Правовая основа', 'material_type': 'noslides', 'material': 'Text_sample'},
             {'lesson_id': 5, 'name': 'Что представляют собой опасные грузы?', 'material_type': 'noslides', 'material': 'Text_sample'},
             {'lesson_id': 6, 'name': 'Общие принципы классификации опасных грузов', 'material_type': 'noslides', 'material': '/static/pdf/posobie_1.pdf'}
           ]

slides = [{'slide_id': 1, 'lesson_id': 3, 'link': '/static/slides/1.jpg'}, {'slide_id': 2, 'lesson_id': 3, 'link': '/static/slides/2.jpg'}, 
          {'slide_id': 3, 'lesson_id': 3, 'link': '/static/slides/3.jpg'}]

lessons_to_courses_data = {1: [1, 2, 3, 4, 5, 6], 
                      2: [1, 2, 3],
                      3: [3, 4],
                      4: [1, 2]}

questions = [{'question_id': 1, 'question_text': 'Test question', 'correctanswer': 'This thing', 'question_type': 'closed'}, 
             {'question_id': 2, 'question_text': 'Test question #2', 'correctanswer': 'Test', 'question_type': 'open'},
             {'question_id': 3, 'question_text': 'Test question #3', 'correctanswer': 'Yes', 'question_type': 'closed'},
             {'question_id': 4, 'question_text': 'Test question #4', 'correctanswer': 'Memes!', 'question_type': 'closed'},
             {'question_id': 5, 'question_text': 'Test question #5', 'correctanswer': 'Testing', 'question_type': 'closed'},
             {'question_id': 6, 'question_text': 'Test question #6', 'correctanswer': 'Nope', 'question_type': 'open'}]

answers = [{'answer_id': 1,  'answer_text': 'This thing'}, 
           {'answer_id': 2, 'answer_text': 'That thing'}, 
           {'answer_id': 3, 'answer_text': 'Other thing'}, 
           {'answer_id': 4, 'answer_text': 'Another thing'}, 
           {'answer_id': 5, 'answer_text': 'Seriously?'}, 
           {'answer_id': 6, 'answer_text': 'Yes'},
           {'answer_id': 7, 'answer_text': 'Memes?'},
           {'answer_id': 8, 'answer_text': 'Memes...'},
           {'answer_id': 9, 'answer_text': 'Memes!'},
           {'answer_id': 10, 'answer_text': 'Testin'},
           {'answer_id': 11, 'answer_text': 'Toastin'},
           {'answer_id': 12, 'answer_text': 'Testing'},
           {'answer_id': 13, 'answer_text': 'Tstng'}
           ]



def extracting_data():
  for check_lesson in lessons_1:
    save_lessons(**check_lesson)
  
  for check_course in courses:
    save_courses(**check_course)

  for check_answer in answers:
    save_answers(**check_answer)

  for check_question in questions:
    save_questions(**check_question)

  for check_slide in slides:
    save_slides(**check_slide)
  

def save_courses(course_id, name):
  courses_exists = Course.query.filter(Course.name == name).count()
  if not courses_exists:
    new_course = Course(id=course_id, name=name)
    new_course.lessons = [Lesson.query.get(x) for x in lessons_to_courses_data[course_id]]
    db.session.add(new_course)
    db.session.commit()
    for course_id, lesson_ids in lessons_to_courses_data.items():
      for order, lesson_id in enumerate(lesson_ids, 1):
        stmt = lessons_to_courses.update().\
          where((lessons_to_courses.c.lesson_id == lesson_id) & (lessons_to_courses.c.course_id  == course_id)).\
          values(order=order)
        db.session.execute(stmt)


def save_lessons(lesson_id, name, material_type, material):
  lessons_exists = Lesson.query.filter(Lesson.name == name).count()
  if not lessons_exists:
    new_lessons = Lesson(id=lesson_id, name=name, material_type=material_type, material=material)
    db.session.add(new_lessons)
    db.session.commit()


def save_answers(answer_id, answer_text):
  answers_exists = AnswerVariant.query.filter(AnswerVariant.answer_text == answer_text).count()
  if not answers_exists:
    new_answers = AnswerVariant(id=answer_id, answer_text=answer_text)
    db.session.add(new_answers)
    db.session.commit()


def save_questions(question_id, question_text, correctanswer, question_type):
  questions_exists = Question.query.filter(Question.question_text == question_text).count()
  if not questions_exists:
    new_question = Question(id=question_id, question_text=question_text, correctanswer=correctanswer, question_type=question_type)
    db.session.add(new_question)
    db.session.commit()


def save_slides(slide_id, lesson_id, link):
  slides_exists = Slide.query.filter(Slide.link == link).count()
  if not slides_exists:
    new_slide = Slide(id=slide_id, lesson_id=lesson_id, link=link)
    db.session.add(new_slide)
    db.session.commit()
