from flask import Blueprint, jsonify
from .AccountRouter import account_blueprint

v1_blueprint = Blueprint('v1', __name__)

@v1_blueprint.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to version 1 of the Movies API!"
    })

# Registers the account routes under this blueprint
v1_blueprint.register_blueprint(account_blueprint, url_prefix='/account')