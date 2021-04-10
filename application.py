from flask import Flask
import numpy as np

application = Flask(__name__)

@application.route('/')
def hello_world():
    return "Yooo"

@application.route('/add')
def add():
    return str(np.add(1,1))
