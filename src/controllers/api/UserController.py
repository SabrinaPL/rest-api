class UserController:
    def __init__(self, logger, user_db_repo):
        self.logger = logger
        self.user_db_repo = user_db_repo

    def delete_user(self, user_id):
        self.logger.info(f"Deleting user {user_id}")

        try:
            self.user_db_repo.delete(user_id)
            self.logger.info(f"User {user_id} deleted successfully")

            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            self.logger.error(f"Error deleting user {user_id}: {e}")
            return {"error": "User deletion failed"}, 500