lessons_to_courses_data = {1: [1, 2, 3, 4, 5, 6], 
                      2: [1, 2, 3],
                      3: [3, 4],
                      4: [1, 2]}

for course_id, lesson_ids in lessons_to_courses_data.items():
      for order, lesson_id in enumerate(lesson_ids, 1):
          print(order)