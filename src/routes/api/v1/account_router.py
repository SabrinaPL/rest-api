from flask import Blueprint

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

    # Log in with a refresh token
    @account_blueprint.route('/users/login/refresh', methods=['POST'])
    def login_refresh():
        return controller.login_refresh_token()

    # Register
    @account_blueprint.route('/users/register', methods=['POST'])
    def register(): 
        return controller.register()

    return account_blueprint