from flask import Blueprint
from flask_jwt_extended import jwt_required

def create_account_blueprint(account_controller, user_controller):
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
        return account_controller.login()

    # Refresh access token
    @account_blueprint.route('/users/refresh', methods=['POST'])
    @jwt_required(refresh=True) # Requires a valid refresh token
    def refresh():
        return account_controller.refresh()

    # Register
    @account_blueprint.route('/users/register', methods=['POST'])
    def register(): 
        return account_controller.register()
    
    # Delete user
    @account_blueprint.route('/users/<user_id>', methods=['DELETE'])
    @jwt_required() # Requires a valid access token
    def delete(user_id):
        """
        Delete a user by ID
        ---
        tags:
          - Users
        summary: Delete a user
        description: Deletes a user from the database using their unique ID.
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            description: The unique ID of the user to delete.
        responses:
          200:
            description: User deleted successfully
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: User deleted successfully
          500:
            description: User deletion failed
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: User deletion failed
        """
        return user_controller.delete_user(user_id)

    return account_blueprint