from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import enum

from src.models import RequestModel, AdModel, UserModel
from src.extensions import auth, db

POST_REQUEST = 1
POST_AD = 1

REQ_STAT_OPEN = 1
REQ_STAT_IN_PROCESS = 2
REQ_STAT_COMPLETED = 3

class CreatePost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help='This field cannot be left blank')

    parser.add_argument('content', type=str, required=True,
                        help='This field cannot be left blank')

    parser.add_argument('price', type=int, required=True,
                        help='This field cannot be left blank')

    parser.add_argument('post_type',  type=int, required=True,
                        help='This field cannot be left blank')

    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        title = data['title']
        content = data['content']
        price = data['price']
        username = data['username']
        post_type = data['post_type']
        # Missing Parameters
        if title is None or content is None or username is None:
            return {'message': 'No title or content or creator passed for create record.'}, 400

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            return {'message': f'User {username} not found.'}, 401

        if post_type == POST_REQUEST:
            request = RequestModel()
            request.title = title
            request.posted_by_id = user.id
            request.content = content
            request.status = REQ_STAT_OPEN
        
            db.session.add(request)
            db.session.commit()
        else:
            ad = AdModel()
            ad.title = title
            ad.posted_by_id = user.id
            ad.content = content
            ad.status = True
        
            db.session.add(ad)
            db.session.commit()

        return {'message': 'Post created.'}, 200