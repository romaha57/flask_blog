from flask import Blueprint, render_template, request, redirect


user_blueprint = Blueprint('profile', __name__,  url_prefix='/user')


@user_blueprint.route('/')
def index_blog():
    return render_template('test1.html')
