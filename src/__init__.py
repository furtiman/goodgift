from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT


import logging
from logging.handlers import WatchedFileHandler

from .extensions import db
from .commands import create_tables
from .security import authenticate, identity

from .api.user import User, UserList
from .api.request import Request, RequestList
from .api.ad import Ad, AdList


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    jwt = JWT(app, authenticate, identity)  # Auto Creates /auth endpoint

    app.config.from_pyfile(config_file)
    api = Api(app)

    db.init_app(app)
    app.cli.add_command(create_tables)  # To interact with app from CLI

    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(RequestList, '/requests')
    api.add_resource(Request, '/requests/<int:req_id>')
    api.add_resource(AdList, '/ads')
    api.add_resource(Ad, '/ads/<int:ad_id>')

    # Logging
    log_level = logging.INFO if app.config['DEBUG'] else logging.ERROR
    handler = WatchedFileHandler('server.log')
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s',
                                  '%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(handler)
    logging.info('\n------------------- Starting Server -------------------')

    return app
