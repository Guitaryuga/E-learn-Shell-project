from webapp import create_app
from webapp.database import extracting_data

"""
Осуществляет запись данных в файл db
"""

app = create_app()
with app.app_context():
    extracting_data()