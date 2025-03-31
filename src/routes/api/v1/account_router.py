from flask import Blueprint
from flask_jwt_extended import jwt_required

def create_account_blueprint(controller):
    """
    Factory function to create the account blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for account-related routes
    account_blueprint = Blueprint('account', __name__)

    # Map HTTP verbs and route paths to controller actions

    # Log in
    @account_blueprint.route('/users/login', methods=['POST'])
    def login():
        return controller.login()

    # Refresh access token
    @account_blueprint.route('/users/refresh', methods=['POST'])
    @jwt_required(refresh=True) # Requires a valid refresh token
    def login_refresh():
        return controller.refresh_token()

    # Register
    @account_blueprint.route('/users/register', methods=['POST'])
    def register(): 
        return controller.register()

    return account_blueprint