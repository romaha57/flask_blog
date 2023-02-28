import os
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from slugify import slugify


from app_user.models import User
from app_user.services import is_image
from config import Settings
from database import db
from .models import Post, Category, Comment, Tag

from .forms import CreateCategoryForm, CreatePostForm, CreateCommentForm

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/categories/<slug_category>/<int:page>')
@blog_blueprint.route('/categories/<slug_category>')
@blog_blueprint.route('/tag/<slug_tag>')
@blog_blueprint.route('/tag/<slug_tag>/<int:page>')
@blog_blueprint.route('/<int:page>')
@blog_blueprint.route('/')
def index_view(page=None, slug_category=None, slug_tag=None):
    if page is None:
        page = request.args.get('page', 1, type=int)

    if slug_category:
        category = Category.query.filter_by(slug=slug_category).first()
        posts = db.session.query(Post).filter_by(category_id=category.id).order_by(Post.created_at).paginate(
            page=page, per_page=2)

    elif slug_tag:
        tag = Tag.query.filter_by(slug=slug_tag).first()
        posts = db.session.query(Post).filter(Post.tags.contains(tag)).order_by(Post.created_at).paginate(
            page=page, per_page=2)

    else:
        posts = db.session.query(Post).paginate(page=page, per_page=2)

    tags = Tag.query.all()
    return render_template('home_page.html', posts=posts, tags=tags, slug_category=slug_category, slug_tag=slug_tag)


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
    categories = Category.query.filter(Category.post != None)
    return render_template('categories.html', categories=categories)


@blog_blueprint.route('/search-result')
def search_result_view():
    search = request.args.get('q')
    tags = Tag.query.all()
    posts = db.session.query(Post).filter(Post.name.contains(search)).order_by(Post.created_at.desc())
    return render_template('home_page.html', posts=posts, tags=tags)


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


@blog_blueprint.route('/post/<post_slug>', methods=('GET', 'POST'))
@login_required
def detail_post_view(post_slug):
    form = CreateCommentForm()
    post = Post.query.filter_by(slug=post_slug).first()
    user = current_user.get_user_from_db()
    all_comment = Comment.query.filter_by(post_id=post.id)
    if request.method == 'POST':
        text_comment = form.text_comment.data
        comment = Comment(
            text_comment=text_comment,
            author_id=user.id,
            post_id=post.id,
            created_at=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', category='success')
        return redirect(url_for('blog.detail_post_view', post_slug=post.slug))
    return render_template('post_detail.html', post=post, form=form, all_comment=all_comment)

