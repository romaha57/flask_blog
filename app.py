from flask import Flask

from app_blog.views import blog_blueprint
from app_user.views import user_blueprint
from config import Settings, toolbar

from database import db, migrate
from admin import admin
from models import User


app = Flask(__name__)
app.config.from_object(Settings)


db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)

toolbar.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(blog_blueprint)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
