from __future__ import print_function
import sys
from flask import Flask
import numpy as np
from flask import request
from flask_cors import CORS, cross_origin
import json
# from .modal_properties import calculate_modal_properties
from main import calculate_bridge_response

application = Flask(__name__)
cors = CORS(application)
application.config["CORS_HEADERS"] = "Content-Type"

@application.route("/hello", methods=["GET"])
@cross_origin()
def hello_world():
    return "HELLLO"


@application.route("/", methods=['POST'])
@cross_origin()
def get_bridge_response():
    data = request.get_json()["data"]
    bridge_displacement, time_vector = calculate_bridge_response(**data)
    return json.dumps(
        {
            "data": {
                "bridge_displacement": list(bridge_displacement),
                "time_vector": list(time_vector),
            }
        }
    )

