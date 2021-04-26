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


# @application.route("/", methods=["POST"])
# @cross_origin()
# def hello_world():
#     data = request.get_json()["data"]
#     (
#         modal_masses,
#         modal_dampings,
#         modal_stiffnesses,
#         circular_frequencies,
#     ) = calculate_modal_properties(**data)
#     print(modal_masses, file=sys.stderr)
#     return json.dumps(
#         {
#             "data": {
#                 "modal_masses": list(modal_masses),
#                 "modal_dampings": list(modal_dampings),
#                 "circular_frequencies": list(circular_frequencies),
#             }
#         }
#     )


@application.route("/", methods=['POST'])
@cross_origin()
def get_bridge_response():
    data = request.get_json()["data"]
    bridge_acceleration, time_vector = calculate_bridge_response(**data)
    return json.dumps(
        {
            "data": {
                "bridge_acceleration": list(bridge_acceleration),
                "time_vector": list(time_vector),
            }
        }
    )

