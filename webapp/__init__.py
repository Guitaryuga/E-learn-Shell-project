from flask import Flask, render_template, url_for

from webapp.database import courses, lessons_1

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def lessons():
        title = "Список курсов"
        return render_template('index_1.html', page_title=title) 

    @app.route("/course/<course_id>")
    def course(course_id):
        for check_id in courses:
            if check_id['course_id'] == course_id:
                title = check_id['name']
                lesson_list = lessons_1
        return render_template('course.html', course_id = course_id, page_title = title, lesson_list = lesson_list)
    
    @app.route("/lesson/<lesson_id>")
    def lesson(lesson_id):
        lesson_list = lessons_1
        for check_lesson in lessons_1:
            if check_lesson['lesson_id'] == lesson_id:
                title = check_lesson['lesson_name']
                material = check_lesson['material']
                if check_lesson['type'] == 'video':
                    return render_template('video_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list) # проба использования разных типов материалов
                elif check_lesson['type'] == 'image':
                    return render_template('image_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list)
                else:
                    return render_template('text_lesson.html', lesson_id = lesson_id, page_title = title, material = material, lesson_list = lesson_list) 
    
    return app

    
   


