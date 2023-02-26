from flask import Flask, render_template
from werkzeug.exceptions import NotFound, BadRequest, RequestEntityTooLarge
from app_blog.views import blog_blueprint
from app_user.views import user_blueprint
from config import Settings, toolbar


from database import db, migrate
from admin import admin
from app_user.models import *
from app_blog.models import *
from app_user.login_config import login_manager
from config import humanize

app = Flask(__name__)
app.config.from_object(Settings)

db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
login_manager.init_app(app)
humanize.init_app(app)


toolbar.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(blog_blueprint)


@app.errorhandler(NotFound)
def error_404_view(error):
    return render_template('error404.html', error=error), 404


@app.errorhandler(BadRequest)
def error_400_view(error):
    return render_template('error400.html', error=error), 400


@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return render_template('error413.html', error=error), 413


if __name__ == '__main__':
    app.run(debug=True, port=8000)
