from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256

from src.models import UserModel

def authenticate(username, password):
    user = UserModel.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password_hash):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)