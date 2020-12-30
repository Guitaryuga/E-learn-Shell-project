from webapp import db, create_app

"""
Создание файла базы данных, DB
"""

db.create_all(app=create_app())