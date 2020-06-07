from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from src.models import UserModel
from src.extensions import auth, db


'''
|   NAME        |     PATH       |   HTTP VERB     |            PURPOSE                   |
|---------------|----------------|-----------------|--------------------------------------|
| Get Users List| /users         |      GET        | Get list of the users                |
| Add User      | /users         |      POST       | Add new user                         |
| Get User      | /users/<int:id>|      GET        | Get a user with id                   |
| Delete User   | /users/<int:id>|      DELETE     | Delete a user with id                |
| Modify User   | /users/<int:id>|      PUT        | Modify a user with id                |
'''


class UserList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
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

    @classmethod
    def get(cls):
        pass


class User(Resource):
    # @jwt_required()
    @classmethod
    def get(cls, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return {'message': 'User not found.'}, 400
        return jsonify({'id': user.id,
                        'username': user.username,
                        'posted_tasks': user.posted_tasks,
                        'completed_tasks': user.completed_tasks})

    @classmethod
    def delete(cls, user_id):
        pass

    @classmethod
    def put(cls, user_id):
        pass
