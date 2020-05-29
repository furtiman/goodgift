from flask import Blueprint, jsonify, request, g, url_for, abort

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .extensions import auth, db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def root_view():
    return '<h1> Hello </h1>'


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@main.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('.get_user', id=user.id, _external=True)})


@main.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@main.route('/api/token')
@auth.login_required
def get_auth_token():
    try:
        token = g.user.generate_auth_token(600)
    except requests.exceptions.RequestException as e:
        logging.error(f'Creating user token is unsuccessful: {e}')

    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@main.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
