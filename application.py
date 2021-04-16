from __future__ import print_function
import sys
from flask import Flask
import numpy as np
from flask import request
from flask_cors import CORS, cross_origin
import json

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

@application.route('/', methods=["POST"])
@cross_origin()
def hello_world():
    data = request.get_json()
    return data

@application.route('/add')
def add():
    return str(np.add(1,1))
