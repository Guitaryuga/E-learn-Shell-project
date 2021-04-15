import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = "sqlite://"
BCRYPT_LOG_ROUNDS = 4
WTF_CSRF_ENABLED = False
TESTING = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY')
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
CKEDITOR_FILE_UPLOADER = 'upload'
UPLOADED_PATH = os.path.join(basedir, 'uploads')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
ADMINS = os.getenv('ADMINS')
