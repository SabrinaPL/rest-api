from flask import Blueprint, jsonify

v1_blueprint = Blueprint('v1', __name__)

@v1_blueprint.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to the RESTful Movies API! API documentation and playground is available at /apidocs",
        "api_version": "1.0.0",
        "documentation": "/apidocs"
    })
