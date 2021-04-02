import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CKEDITOR_FILE_UPLOADER = 'upload'
UPLOADED_PATH = os.path.join(basedir, 'uploads')
