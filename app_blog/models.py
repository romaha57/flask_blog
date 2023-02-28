from datetime import datetime

from slugify import slugify
from sqlalchemy import func, event

from database import db
from app_user.models import *


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    count_views = db.Column(db.Integer, default=0)
    image = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='tags_cloud', backref='posts')

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def __repr__(self):
        return f'<Post -  {self.name}>'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text_comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment -  {self.author_id.name}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    post = db.relationship('Post', backref='category', lazy=True)
    photo = db.Column(db.String)

    def __repr__(self):
        return f'<Category -  {self.name}>'


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def __repr__(self):
        return f'<Tag -  {self.name}>'


tags_cloud = db.Table('tags_cloud',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


event.listen(Tag.name, 'set', Tag.slugify, retval=False)
event.listen(Post.name, 'set', Post.slugify, retval=False)

