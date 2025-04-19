from flask import Blueprint
from flask_jwt_extended import jwt_required

def create_account_blueprint(account_controller, user_controller):
    """
    Factory function to create the account blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for account-related routes
    account_blueprint = Blueprint('account', __name__)

    # Log in
    @account_blueprint.route('/users/login', methods=['POST'])
    def login():
        """
        Log in a user
        ---
        tags:
          - Users
        summary: Log in a user
        description: Authenticates a user and returns a JWT access token and refresh token.
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user.
                  example: johndoe
                password:
                  type: string
                  description: The password of the user.
                  example: password123
        responses:
          200:
            description: User logged in successfully
          400:
            description: Invalid credentials
          500:
            description: Internal server error
        """
        return account_controller.login()

    # Refresh access token
    @account_blueprint.route('/users/refresh', methods=['POST'])
    @jwt_required(refresh=True) # Requires a valid refresh token
    def refresh():
        """
        Refresh the access token
        ---
        tags:
          - Users
        summary: Refresh the access token
        description: Generates a new access token using a valid refresh token.
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                refresh_token:
                  type: string
                  description: The refresh token to generate a new access token.
                  example: "sample_refresh_token"
        responses:
          200:
            description: Token refreshed successfully
          400:
            description: Invalid refresh token
          500:
            description: Internal server error
        """
        return account_controller.refresh()

    # Register
    @account_blueprint.route('/users/register', methods=['POST'])
    def register(): 
        """
        Register a new user
        ---
        tags:
          - Users
        summary: Register a new user
        description: Creates a new user account with the provided details.
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                first_name:
                  type: string
                  description: The first name of the user.
                last_name:
                  type: string
                  description: The last name of the user.
                username:
                  type: string
                  description: The unique username of the user.
                password:
                  type: string
                  description: The password of the user.
                email:
                  type: string
                  description: The email address of the user.
        responses:
          201:
            description: User registered successfully
          400:
            description: Invalid input data
          500:
            description: Internal server error
        """
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
        description: Deletes a user from the database using their unique ID. Requires a valid JWT access token.
        security:
          - BearerAuth: []
        parameters:
          - name: Authorization
            in: header
            required: true
            schema:
              type: string
              description: Bearer JWT token for authentication.
          - name: user_id
            in: path
            required: true
            schema:
              type: string
              description: The unique ID of the user to delete.
        responses:
          204:
            description: User deleted successfully
          400:
            description: Invalid or missing user ID
          500:
            description: User deletion failed
        """
        return user_controller.delete_user(user_id)

    return account_blueprint