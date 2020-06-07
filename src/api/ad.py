from flask import Blueprint, jsonify, request, g, url_for, abort
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import enum

from src.models import RequestModel, AdModel, UserModel
from src.extensions import auth, db

'''
|   NAME      |     PATH     |   HTTP VERB     |            PURPOSE                 |
|-------------|--------------|-----------------|------------------------------------|
| Get Ads List| /ads         |      GET        | Get list of the ads                |
| Add Ad      | /ads         |      POST       | Add new ad                         |
| Get Ad      | /ads/<int:id>|      GET        | Get a ad with id                   |
| Delete Ad   | /ads/<int:id>|      DELETE     | Delete a ad with id                |
| Modify Ad   | /ads/<int:id>|      PUT        | Modify a ad with id                |
'''


class AdList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('content', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('price', type=int, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
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

        ad = AdModel()
        ad.title = title
        ad.posted_by_id = user.id
        ad.content = content
        ad.status = 1

        db.session.add(ad)
        db.session.commit()

        return {'message': 'Ad created.'}, 200

    def get(self):
        pass


class Ad(Resource):

    def get(self, ad_id):
        pass

    def delete(self, ad_id):
        pass

    def put(self, ad_id):
        pass
