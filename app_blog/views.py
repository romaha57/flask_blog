from flask import Blueprint, request, render_template, redirect


blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/')
def index_blog():
    return render_template('test2.html')
