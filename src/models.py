import jwt
import time
from passlib.hash import pbkdf2_sha256
import enum

from .extensions import db
from .settings import SECRET_KEY


class UserModel(db.Model):
    '''
    Class representing a user
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(256))
    posted_tasks = db.Column(db.Integer)
    completed_tasks = db.Column(db.Integer)

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, SECRET_KEY,
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])


class AdModel(db.Model):
    '''
    Class representing an advertisement post
    '''
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.String(256))
    price = db.Column(db.Integer)
    status = db.Column(db.Integer) # Active = 1 / Not active = 0
    posted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    responded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class RequestModel(db.Model):
    '''
    Class representing a help request
    '''
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.String(256))
    price = db.Column(db.Integer)
    posted_at = db.Column(db.DateTime())
    status = db.Column(db.Integer)
    posted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
