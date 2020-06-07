from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from src.models import RequestModel, AdModel, UserModel
from src.extensions import auth, db

REQ_STAT_OPEN = 1
REQ_STAT_IN_PROCESS = 2
REQ_STAT_COMPLETED = 3

'''
|   NAME        |     PATH          |   HTTP VERB     |               PURPOSE                   |
|---------------|-------------------|-----------------|-----------------------------------------|
| Get Reqs List | /requests         |      GET        | Get list of the request                 |
| Add Request   | /requests         |      POST       | Add new request                         |
| Get Request   | /requests/<int:id>|      GET        | Get a request with id                   |
| Delete Request| /requests/<int:id>|      DELETE     | Delete a request with id                |
| Modify Request| /requests/<int:id>|      PUT        | Modify a request with id                |
'''


class RequestList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('content', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('price', type=int, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        title = data['title']
        content = data['content']
        price = data['price']
        username = data['username']
        # Missing Parameters
        if title is None or content is None or username is None:
            return {'message': 'No title or content or creator passed for create record.'}, 400

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {'message': f'User {username} not found.'}, 401

        request = RequestModel()
        request.title = title
        request.posted_by_id = user.id
        request.content = content
        request.status = REQ_STAT_OPEN

        db.session.add(request)
        db.session.commit()

        return {'message': 'Request created.'}, 200

    @classmethod
    def get(cls):
        pass


class Request(Resource):

    @classmethod
    def get(cls, req_id):
        pass

    @classmethod
    def delete(cls, req_id):
        pass

    @classmethod
    def put(cls, req_id):
        pass
