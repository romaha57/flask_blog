import os

import werkzeug.exceptions
from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from slugify import slugify

from app_user.models import User
from app_user.services import is_image
from config import Settings
from database import db
from .models import Post, Category, Comment, Tag, tags_cloud

from .forms import CreateCategoryForm, CreatePostForm


blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/')
def index_view():
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template('home_page.html', posts=posts, tags=tags)


@blog_blueprint.route('/create-post', methods=('POST', 'GET'))
@login_required
def create_post_view():
    form = CreatePostForm()
    if form.validate_on_submit():
        file = request.files.get('image')
        file_ext = '.' + file.filename.split('.')[-1]
        path_to_file = os.path.join(Settings.UPLOAD_PATH, f'post_photo/{form.name.data}{file_ext}')

        if is_image(file.stream) and file_ext == is_image(file.stream):
            category = Category.query.filter_by(name=form.category.data).first()
            user = User.query.get(current_user.get_id())
            all_tags = [Tag.query.filter_by(name=tag_name).first() for tag_name in form.tags.data]
            post = Post(
                name=form.name.data,
                slug=slugify(form.name.data),
                description=form.description.data,
                image=f'post_photo/{form.name.data}{file_ext}',
                author_id=user.id,
                category_id=category.id
            )

            for tag in all_tags:
                post.tags.append(tag)

            db.session.add(post)
            db.session.commit()

            file.save(path_to_file)
            flash('Пост добавлен', category='success')
            return redirect(url_for('blog.index_view'))

    return render_template('create_post.html', form=form)


@blog_blueprint.route('/categories')
def category_view():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@blog_blueprint.route('/categories/<slug_category>')
def posts_by_category(slug_category):
    # categories = Post.query.filter(slug=slug_category)
    return render_template('home_page.html')


@blog_blueprint.route('/search-result')
def search_result_view():
    result = request.args.get('q')
    return render_template('search_result.html', result=result)


@blog_blueprint.route('/create-category', methods=('POST', 'GET'))
@login_required
def create_category_view():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        slug = slugify(name)
        file = request.files.get('photo')
        file_ext = '.' + file.filename.split('.')[-1]
        path_to_file = os.path.join(Settings.UPLOAD_PATH, f'category_photo/{name}{file_ext}')

        if is_image(file.stream) and file_ext == is_image(file.stream):
            category = Category(
                name=name,
                slug=slug,
                photo=f'category_photo/{name}{file_ext}'
            )

            db.session.add(category)
            db.session.commit()
            file.save(path_to_file)
            flash('Категория добавлена', category='success')
        else:
            flash('Ошибка при загрузке файла', category='danger')

    return render_template('create_category.html', form=form)




