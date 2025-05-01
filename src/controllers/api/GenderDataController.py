from flask import request, jsonify, make_response
from utils.CustomErrors import CustomError

class GenderDataController:
    def __init__(self, logger, gender_data_db_repo, gender_data_query_service):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.gender_data_query_service = gender_data_query_service
                 
def get_gender_data(self):
    """
    Fetches all gender data from the database.
    """
    # try:
      
      
    # except CustomError as e:
    #   self.logger.error(f"Custom error occurred: {e.message}")
    #   raise e
    # except Exception as e:
    #   self.logger.error(f"Error fetching gender data: {e}")