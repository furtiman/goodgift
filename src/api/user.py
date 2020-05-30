from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from src.models import UserModel
from src.extensions import auth, db

'''
|   NAME      |     PATH       |   HTTP VERB     |            PURPOSE                   |
|----------   |----------------|-----------------|--------------------------------------|
|Get API Token| /token         |      GET        | Get a token for the user             |
| Add User    | /users         |      POST       | Create a new user                    |
| Get User    | /users/<int:id>|      GET        | Get a user with id                   |
| New         | /blog/new      |      GET        | Shows new form for new blog entry    |
| Create      | /blog          |      POST       | Creates a new blog post              |
| Show        | /blog/:id      |      GET        | Shows one specified blog post        |
| Edit        | /blog/:id/edit |      GET        | Shows edit form for one blog post    |
| Update      | /blog/:id      |      PUT        | Updates a particular blog post       |
| Destroy     | /blog/:id      |      DELETE     | Deletes a particular blog post       |
'''


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        # Missing Parameters
        if username is None or password is None:
            return {'message': 'No username or password passed for registration.'}, 400
        # Existing User
        if UserModel.query.filter_by(username=username).first() is not None:
            return {'message': 'UserModel has already been created, aborting.'}, 400

        user = UserModel(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        return {'username': user.username}, 201


class UserList(Resource):
    def get():
        pass


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return {'message': 'User not found.'}, 400
        return jsonify({'id': user.id,
                        'username': user.username,
                        'posted_tasks': user.posted_tasks,
                        'completed_tasks': user.completed_tasks})
