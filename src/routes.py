from flask import Blueprint
from .models import User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def root_view():
    return '<h1> Hello </h1>'
