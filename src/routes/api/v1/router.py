from flask import Blueprint, jsonify

v1_blueprint = Blueprint('v1', __name__)

@v1_blueprint.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to version 1 of the Movies API!"
    })
