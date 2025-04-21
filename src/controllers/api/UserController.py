from flask import jsonify, make_response
from utils.CustomErrors import CustomError
from utils.custom_status_codes import USER_CUSTOM_STATUS_CODES

class UserController:
    def __init__(self, logger, user_db_repo):
        self.logger = logger
        self.user_db_repo = user_db_repo

    def delete_user(self, user_id):
        self.logger.info(f"Attempting to delete user with ID: {user_id}")

        # Validate input
        if not user_id:
            self.logger.error("User ID is missing")
            raise CustomError(USER_CUSTOM_STATUS_CODES[400]["missing_user_id"], 400)

        try:
            # Check if the user exists
            user = self.user_db_repo.find_by_id(user_id)

            if not user:
                self.logger.warning(f"User with ID {user_id} not found")
                raise CustomError(USER_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

            # Delete the user
            self.user_db_repo.delete(user_id)
            self.logger.info(f"User {user_id} deleted successfully")

            response = {
                "message": "User deleted successfully"
            }
            return make_response(jsonify(response), 204)

        except CustomError as e:
            self.logger.error(f"Custom error occurred: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error while deleting user {user_id}: {e}")
            raise e