import os.path
from datetime import datetime

from sqlalchemy import func

from database import db
from app_blog.models import *


def get_default_status():
    user_status_default = UserStatus.query.get(1)
    return user_status_default.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hash_password = db.Column(db.String, nullable=False, unique=True)
    avatar = db.Column(db.String)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), default=get_default_status)
    created_at = db.Column(db.DateTime, server_default=func.now())
    comments = db.relationship('Comment',  backref='author', lazy=True)
    posts = db.relationship('Post',  backref='author', lazy=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User -  {self.name}>'


class UserStatus(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    count_posts = db.Column(db.Integer, default=0)
    user_id = db.relationship('User', backref='status', lazy=True)

    def __repr__(self):
        return f'<Status {self.name}>'
