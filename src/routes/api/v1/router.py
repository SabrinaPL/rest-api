from flask import Blueprint, jsonify
# from .account_router import account_blueprint

v1_blueprint = Blueprint('v1', __name__)

@v1_blueprint.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to version 1 of the Movies API!",
        "endpoints": {
            "register": "/api/v1/account/register",
            "login": "/api/v1/account/login",
            "login/refresh": "/api/v1/account/login/refresh",
            "movies": "/api/v1/movies",
            "actors": "/api/v1/actors",
            "ratings": "/api/v1/ratings"
        }
    })

# Registers the account routes under this blueprint
# v1_blueprint.register_blueprint(account_blueprint, url_prefix='/account')