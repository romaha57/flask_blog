from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app_blog.models import  Comment, Post, Tag
from app_user.models import User, UserStatus
from database import db


class CustomModelView(ModelView):
    page_size = 20
    # column_list = ('name', User.last_name)
    # column_searchable_list = ['name', 'email']
    # column_filters = ['country']
    # column_editable_list = ['name', 'last_name']


admin = Admin()
admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(UserStatus, db.session))
admin.add_view(CustomModelView(Post, db.session))
admin.add_view(CustomModelView(Comment, db.session))
admin.add_view(CustomModelView(Tag, db.session))
