from flask import request, jsonify, make_response
from utils.CustomErrors import CustomError
from utils.custom_status_codes import GENDER_DATA_CUSTOM_STATUS_CODES

class GenderDataController:
    def __init__(self, logger, gender_data_db_repo, gender_data_query_service):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.gender_data_query_service = gender_data_query_service
                 
    def get_gender_data(self):
        """
        Fetches all gender data from the database.
        """
        try:
        # TODO: Implement pagination and add max per page for optimization. Other options, caching? Check indexing in MongoDB!  
          
        # Get potential query parameters from the request
          query_params = request.args.to_dict()
          self.logger.info(f"Query parameters received: {query_params}")
      
          # Extract and validate pagination parameters
          try:
            page = int(query_params.pop('page', 1))
            per_page = int(query_params.pop('per_page', 20))

            if page < 1 or per_page < 1:
              raise ValueError("Page and per_page must be greater than 0")
          except ValueError:
            self.logger.error("Invalid pagination parameters")
            raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[400]["invalid_pagination"], 400)

          if query_params:
            self.logger.info("Query parameters provided, fetching gender statistics data by filter...")
      
            # Validate the query parameters
            # query = self.gender_data_query_service.build_query('movies', query_params)
            self.logger.info("Query built successfully")
          else: 
            self.logger.info("Query parameters not provided, fetching all gender statistics...")
            query = {}
        
          gender_data = self.gender_data_db_repo.find_by_query(query)
      
          if not gender_data:
            self.logger.info("No gender statistics data found")
            raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[404]["no_gender_data_found"], 404)
      
          self.logger.info(f"Found {len(gender_data)} gender statistics records")
      
          gender_statistics_json = [
              {
              "id": str(gender_data.id),
              "movie_id": gender_data.movie_id,
              "title": gender_data.title,
              "release_date": gender_data.release_date if gender_data.release_date else None,
              "countries": [country.name if hasattr(country, 'name') else country for country in gender_data.countries],
              "companies": [company.name if hasattr(company, 'name') else company for company in gender_data.companies],
              "genres": [genre.name if hasattr(genre, 'name') else genre for genre in gender_data.genres],
              "department": gender_data.department,
              "gender": gender_data.gender,
              "name": gender_data.name,
            }
            for gender_data in gender_data 
          ] 
    
          # Create pagination links
      
          response = {
            "message": "Gender statistics data fetched successfully",
            "total": len(gender_data),
            "gender_statistics": gender_statistics_json,
          }
      
          return make_response(jsonify(response), 200)

        except CustomError as e:
          self.logger.error(f"Custom error occurred: {e.message}")
          raise e
        except Exception as e:
          self.logger.error(f"Error fetching gender data: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)