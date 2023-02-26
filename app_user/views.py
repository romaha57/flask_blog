import os.path

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wtforms import ValidationError

from config import Settings
from .forms import LoginUserForm, RegisterUserForm, RestorePasswordForm, UploadAvatarUser
from .services import check_password, is_image
from .models import User
from database import db
from .login_config import UserLogin


user_blueprint = Blueprint('account', __name__,  url_prefix='/account')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter(User.email==email).first()
        if user and check_password_hash(user.hash_password, password):
            user_login = UserLogin().create(user)
            if form.is_remember.data:
                login_user(user_login, remember=True)
            else:
                login_user(user_login)
            return redirect(url_for('blog.index_view'))

        else:
            flash('Введен неверный email/пароль', category='danger')

    return render_template('login.html', form=form)


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_view():
    form = RegisterUserForm()

    if form.validate_on_submit():
        check_user_in_db = db.session.query(User).filter(db.or_(User.email==form.email.data,
                                                                User.name==form.name.data)).first()
        if check_user_in_db:
            flash('Пользователь с таким Email/Имя уже существует', category='danger')
            return render_template('signup.html', form=form)

        message, is_checked = check_password(password=form.password.data)

        if not is_checked:
            flash(message, category='danger')
            return render_template('signup.html', form=form)

        user = User(
            name=form.name.data,
            email=form.email.data,
            hash_password=generate_password_hash(form.password.data),
        )
        if form.name.data == 'admin':
            user.is_admin = True

        db.session.add(user)
        db.session.commit()

        flash('Вы успешно зарегистрировались<br>Пожалуйста авторизуйтесь', category='success')
        return redirect(url_for('account.login_view'))

    return render_template('signup.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('blog.index_view'))


@user_blueprint.route('/profile/<username>', methods=('POST', 'GET'))
@login_required
def profile_view(username):
    form = UploadAvatarUser()
    if form.validate_on_submit():
        file = request.files.get('avatar')
        file_ext = '.' + file.filename.split('.')[-1]
        path_to_file = os.path.join(Settings.UPLOAD_PATH, f'avatars/{current_user.get_id()}{file_ext}')

        if is_image(file.stream) and file_ext == is_image(file.stream):
            current_user.get_user_from_db().avatar = f'avatars/{current_user.get_id()}{file_ext}'
            db.session.commit()
            file.save(path_to_file)
        else:
            flash('Ошибка при загрузке файла', category='danger')

    user = db.session.query(User).filter(User.name==username).first()
    return render_template('profile.html', user=user, form=form)


@user_blueprint.route('/profile/<username>/change-password', methods=['GET', 'POST'])
@login_required
def change_password_view(username):
    user = db.session.query(User).filter(User.name==username).first()
    form = RestorePasswordForm()
    if form.validate_on_submit():
        message, is_checked = check_password(password=form.new_password.data)

        if not is_checked:
            flash(message, category='danger')
            return render_template('change_password.html', user=user, form=form)

        if check_password_hash(user.hash_password, form.old_password.data):
            user.hash_password = generate_password_hash(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash('Пароль успешно изменен', category='success')

            return redirect(url_for('account.profile_view', username=username))

        flash('Старый пароль неверный', category='danger')

    return render_template('change_password.html', user=user, form=form)


@user_blueprint.route('/media/<path:filename>')
@login_required
def media(filename):
    return send_from_directory(Settings.UPLOAD_PATH, filename)

