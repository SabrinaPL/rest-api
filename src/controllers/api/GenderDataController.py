from flask import request, jsonify, make_response
from utils.CustomErrors import CustomError
from utils.custom_status_codes import GENDER_DATA_CUSTOM_STATUS_CODES

class GenderDataController:
    def __init__(self, logger, gender_data_db_repo, gender_statistics_service, generate_hateoas_links):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.gender_statistics_service = gender_statistics_service
      self.generate_hateoas_links = generate_hateoas_links
                 
    def get_gender_data(self):
        """
        Fetches all gender data from the database with custom or default pagination. Can be filtered by query parameters.
        """
        try:
        # Get potential query parameters from the request
          query_params = request.args.to_dict()
          self.logger.info(f"Query parameters received: {query_params}")

          # Extract and validate pagination parameters
          page = int(query_params.pop('page', 1))
          per_page = int(query_params.pop('per_page', 100))

          if page < 1 or per_page < 1:
            raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[400]["invalid_pagination"], 400)
          if per_page > 100:
            self.logger.warning("per_page exceeds maximum limit of 100, setting to 100")
            per_page = 100

          # Fetch total records for pagination
          query = {}  
          total_records = self.gender_data_db_repo.find_by_query(query).count()
          self.logger.info(f"Total records found: {total_records}")
        
          gender_data = self.gender_data_db_repo.find_by_query_with_pagination(query, page=page, per_page=per_page)
      
          if not gender_data:
            self.logger.info("No gender statistics data found")
            raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[404]["no_gender_data_found"], 404)
      
          self.logger.info(f"Found {len(gender_data)} gender statistics records")
      
          gender_statistics_json = [
              {
              "id": str(gender_data.id),
              "movie_id": gender_data.movie_id,
              "title": gender_data.title,
              "year": gender_data.year if gender_data.year else None,
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
          pagination_links = self.generate_hateoas_links.create_pagination_links("gender_statistics.get_gender_data", page, per_page, total_records)
          self.logger.info("Pagination links generated")
      
          response = {
            "message": "Gender statistics data fetched successfully",
            "total": len(gender_data),
            "gender_statistics": gender_statistics_json,
            "_links": {
              **pagination_links
            }
          }

          return make_response(jsonify(response), 200)

        except CustomError as e:
          self.logger.error(f"Custom error occurred: {e}")
          raise e
        except Exception as e:
          self.logger.error(f"Error fetching gender data: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def get_gender_statistics_by_country(self):
      """
      Get gender statistics data by specific country.
      """
      try:
        # Get potential query parameters from the request
        query_params = request.args.to_dict()
        self.logger.info(f"Query parameters received: {query_params}")
        country = query_params.get('country')
      
        if not query_params or country is None:
          self.logger.info("No country provided, fetching all gender statistics data for movie production countries")
          
          return self.gender_statistics_service.get_gender_statistics_by_country()
        
        self.logger.info(f"Fetching gender statistics data for country: {country}")
        
        return self.gender_statistics_service.get_gender_statistics_by_country(country)
      
      except CustomError as e:
        self.logger.error(f"Custom error occurred: {e}")
        raise e 
      except Exception as e:
        self.logger.error(f"Error fetching data by country: {e}")
        raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
      
    def get_gender_statistics_by_company(self):
      """
      Get gender statistics data by specific production company.
      """
      try:
        # Get potential query parameters from the request
        query_params = request.args.to_dict()
        self.logger.info(f"Query parameters received: {query_params}")
        company = query_params.get('company')
        
        if not query_params or company is None:
          self.logger.info("No production company provided, fetching all gender statistics data for movie production companies")
            
          return self.gender_statistics_service.get_gender_statistics_by_company()
        
        self.logger.info(f"Fetching gender statistics data for production company: {company}")
        
        return self.gender_statistics_service.get_gender_statistics_by_company(company)
      
      except CustomError as e:
        self.logger.error(f"Custom error occurred: {e}")
        raise e
      except Exception as e:
        self.logger.error(f"Error fetching data by production company: {e}")
        raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
      
    def get_gender_statistics_by_genre(self):
      """
      Get gender statistics data by specific movie genre.
      """
      try:
        # Get potential query parameters from the request
        query_params = request.args.to_dict()
        self.logger.info(f"Query parameters received: {query_params}")
        genre = query_params.get('genre')
        
        if not query_params or genre is None:
          self.logger.info("No movie genre provided, fetching gender statistics data for all movie genres")
          
          return self.gender_statistics_service.get_gender_statistics_by_genre()
        
        self.logger.info(f"Fetching gender statistics data for movie genre: {genre}")
        
        return self.gender_statistics_service.get_gender_statistics_by_genre(genre)
      
      except CustomError as e:
        self.logger.error(f"Custom error occurred: {e}")
        raise e
      except Exception as e:
        self.logger.error(f"Error fetching data by movie genre: {e}")
        raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
      
    def get_gender_statistics_by_department(self):
      """
      Get gender statistics data by specific department.
      """
      try:
        # Get potential query parameters from the request
        query_params = request.args.to_dict()
        self.logger.info(f"Query parameters received: {query_params}")
        department = query_params.get('department')
        
        if not query_params or department is None:
          self.logger.info("No department provided, fetching gender statistics data for all departments")
          
          return self.gender_statistics_service.get_gender_statistics_by_department()
        
        self.logger.info(f"Fetching gender statistics data for department: {department}")
        
        return self.gender_statistics_service.get_gender_statistics_by_department(department)
      
      except Exception as e:
        self.logger.error(f"Error fetching data by department: {e}")
        raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
      
    def get_gender_statistics_by_year(self):
      """
      Get gender statistics data by specific production year.
      """
      try:
        # Get potential query parameters from the request
        query_params = request.args.to_dict()
        self.logger.info(f"Query parameters received: {query_params}")
        year = query_params.get('year')
        
        if not query_params or year is None:
          self.logger.info("No production year provided, fetching gender statistics data for all production years")
          
          return self.gender_statistics_service.get_gender_statistics_by_year()
        
        self.logger.info(f"Fetching gender statistics data for production year: {year}")
        
        return self.gender_statistics_service.get_gender_statistics_by_year(year)
      
      except CustomError as e:
        self.logger.error(f"Custom error occurred: {e}")
        raise e
      except Exception as e:
        self.logger.error(f"Error fetching data by production year: {e}")
        raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
        
        
      