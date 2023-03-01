import os

from dotenv import load_dotenv
from flask_debugtoolbar import DebugToolbarExtension
from flask_humanize import Humanize

load_dotenv()


class Settings:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_ADMIN_SWATCH = 'cerulean'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    PER_PAGE = 10

    UPLOAD_PATH = 'media'

    # 1 Mb
    MAX_CONTENT_LENGTH = 1024 * 1024


toolbar = DebugToolbarExtension()
humanize = Humanize()


@humanize.localeselector
def get_locale():
    return 'ru_RU'
