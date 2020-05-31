from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from src.models import RequestModel, UserModel
from src.extensions import auth, db

class CreateRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('content', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('type', type=int, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        title = data['title']
        type_of_post = data['type']
        content = data['content']
        username = data['username']
        # Missing Parameters
        if title is None or content is None or username is None:
            return {'message': 'No title or content or creator passed for create record.'}, 400

        user = UserModel.query.filter_by(username=username).first()
        request = RequestModel()
        request.title = title
        request.posted_by_id = user.id
        request.content = content
        
        db.session.add(request)
        db.session.commit()

        return {'username': user.username}, 200