from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (FileField, SelectField, SelectMultipleField, StringField,
                     TextAreaField)
from wtforms.validators import InputRequired

from .utils import get_categories_for_choice, get_tags_for_choice


class CreatePostForm(FlaskForm):
    name = StringField(validators=(InputRequired(), ))
    image = FileField(
        validators=(FileAllowed(('png', 'jpg', 'jpeg'),
                                message='Недопустимый формат изображения(.png, .jpg, .jpeg)'),
                    FileRequired(message='Изображение не добавлено')))
    description = TextAreaField(validators=(InputRequired(), ))
    category = SelectField('Выберите категорию', choices=get_categories_for_choice,
                           validators=(InputRequired(),))
    tags = SelectMultipleField('Выберите теги', choices=get_tags_for_choice,
                               validators=(InputRequired(),))


class CreateCommentForm(FlaskForm):
    text_comment = StringField('Комментарий')


class CreateCategoryForm(FlaskForm):
    name = StringField(validators=(InputRequired(),))
    photo = FileField('Обложка категории',
                      validators=(FileAllowed(('png', 'jpg', 'jpeg'),
                                              message='Недопустимый формат изображения(.png, .jpg, .jpeg)'), ))


class CreateTagForm(FlaskForm):
    name = StringField(validators=(InputRequired(),))
