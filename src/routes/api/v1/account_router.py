from flask import Blueprint, request, jsonify
from controllers.api.AccountController import AccountController

# Create a Blueprint for account-related routes
account_blueprint = Blueprint('account', __name__)

# Instantiate the controller
controller = AccountController()

# Map HTTP verbs and route paths to controller actions

# Log in
@account_blueprint.route('/login', methods=['POST'])
def login():
    return controller.login(request)

# Log in with a refresh token
@account_blueprint.route('/login/refresh', methods=['POST'])
def login_refresh():
    return controller.login_refresh_token(request)

# Register
@account_blueprint.route('/register', methods=['POST'])
def register():
    return controller.register(request)