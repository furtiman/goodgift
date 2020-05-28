from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler
import io
import json

from flask import Flask

import requests
from requests.adapters import HTTPAdapter

SERVER_PORT = 5000

DEBUG = True

# Create a flask application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_view():
    return '<h1> Hello </h1>'

if __name__ == "__main__":
    # Logging
    log_level = logging.INFO if DEBUG else logging.ERROR
    handler = logging.handlers.WatchedFileHandler('server.log')
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s',
                                  '%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(log_level)
    root.addHandler(handler)
    logging.info('\n------------------- Starting Server -------------------')

    app.run(threaded=True, port=SERVER_PORT)
