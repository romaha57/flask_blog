
from app_blog.models import Category, Tag
from database import db


def get_categories_for_choice():
    from app import app
    with app.app_context():
        categories = db.session.query(Category).all()
        choice_categories = [(category.name, category.name) for category in categories]
        return choice_categories


def get_tags_for_choice():
    from app import app
    with app.app_context():
        tags = db.session.query(Tag).all()
        choice_tags = [(tag.name, tag.name) for tag in tags]
        return choice_tags

