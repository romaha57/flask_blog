import os

from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv


load_dotenv()


class Settings:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_ADMIN_SWATCH = 'cerulean'


toolbar = DebugToolbarExtension()
