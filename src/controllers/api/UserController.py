from flask import jsonify, make_response
from utils.CustomErrors import CustomError, NotFoundError

class UserController:
    def __init__(self, logger, user_db_repo):
        self.logger = logger
        self.user_db_repo = user_db_repo

    def delete_user(self, user_id):
        self.logger.info(f"Attempting to delete user with ID: {user_id}")

        # Validate input
        if not user_id:
            self.logger.error("User ID is missing")
            raise CustomError("User ID is required", 400)

        try:
            # Check if the user exists
            user = self.user_db_repo.find_by_id(user_id)
            if not user:
                self.logger.warning(f"User with ID {user_id} not found")
                raise NotFoundError(f"User with ID {user_id} not found")

            # Delete the user
            self.user_db_repo.delete(user_id)
            self.logger.info(f"User {user_id} deleted successfully")

            response = {
                "message": "User deleted successfully"
            }
            return make_response(jsonify(response), 200)

        except NotFoundError as e:
            self.logger.warning(str(e))
            raise e

        except Exception as e:
            self.logger.error(f"Unexpected error while deleting user {user_id}: {e}")
            raise CustomError("Internal server error", 500)