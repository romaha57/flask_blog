from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, EmailField, PasswordField, BooleanField, FileField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired


class RegisterUserForm(FlaskForm):
    name = StringField('Имя', validators=(DataRequired(), Length(min=4, max=40)))
    email = EmailField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Пароль', validators=(DataRequired(),))
    password_repeat = PasswordField('Пароль: ', validators=(DataRequired(), EqualTo('password', message='Пароли должны совпадать')))
    submit = SubmitField('Зарегистрироваться')


class LoginUserForm(FlaskForm):
    email = EmailField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Пароль', validators=(DataRequired(),))
    is_remember = BooleanField('Запомнить?', default=True)


class RestorePasswordForm(FlaskForm):
    old_password = PasswordField(validators=(DataRequired(),))
    new_password = PasswordField(validators=(DataRequired(),))
    new_password_repeat = PasswordField('Пароль: ', validators=(DataRequired(), EqualTo('new_password', message='Пароли должны совпадать')))


class UpdateUserInfoForm(FlaskForm):
    pass


class UploadAvatarUser(FlaskForm):
    avatar = FileField('Фото профиля: ', validators=(FileAllowed(('png', 'jpg', 'jpeg'), message='Недопустимый формат изображения(.png, .jpg, .jpeg)'),))
    submit = SubmitField('Изменить фото')


