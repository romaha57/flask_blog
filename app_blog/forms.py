from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, FileField, TextAreaField, SelectField, SelectMultipleField


from app_blog.models import Category, Tag
from database import db

from .utils import get_categories_for_choice, get_tags_for_choice


class CreatePostForm(FlaskForm):
    name = StringField()
    image = FileField(
        validators=(FileAllowed(('png', 'jpg', 'jpeg'), message='Недопустимый формат изображения(.png, .jpg, .jpeg)'), FileRequired(message='Изображение не добавлено')))
    description = TextAreaField()
    category = SelectField('Выберите категорию', choices=get_categories_for_choice)
    tags = SelectMultipleField('Выберите теги', choices=get_tags_for_choice)


class CreateCommentForm(FlaskForm):
    pass


class SearchForm(FlaskForm):
    name = StringField()


class CreateCategoryForm(FlaskForm):
    name = StringField()
    photo = FileField(validators=(FileAllowed(('png', 'jpg', 'jpeg'), message='Недопустимый формат изображения(.png, .jpg, .jpeg)'), ))
