from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from database import db


class CustomModelView(ModelView):
    page_size = 20
    # column_list = ('name', User.last_name)
    # column_searchable_list = ['name', 'email']
    # column_filters = ['country']
    # column_editable_list = ['name', 'last_name']


admin = Admin()
