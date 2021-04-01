import os

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CKEDITOR_FILE_UPLOADER = 'upload'
UPLOADED_PATH = os.getenv('UPLOADED_PATH')
