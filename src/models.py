import jwt
import time
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions  import db
from .settings import SECRET_KEY

class User(db.Model):
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
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
