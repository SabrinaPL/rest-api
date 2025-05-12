from utils.CustomErrors import CustomError
from utils.custom_status_codes import GENDER_DATA_CUSTOM_STATUS_CODES

class GenderStatisticsService:
    def __init__(self, logger, gender_data_db_repo, aggregation_pipeline_service):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.aggregation_pipeline_service = aggregation_pipeline_service

    def get_gender_statistics_by_country(self, country=None):
        """
        Retrieve gender statistics data by production country.
        """
        self.logger.info("Retrieving gender statistics data by country...")

        try:
          # Call the aggregation pipeline service to get the pipeline
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_country(country)
        
          return self.execute_aggregation_pipeline(pipeline)
        except Exception as e:
          self.logger.error(f"Error retrieving data by country: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
    def get_gender_statistics_by_company(self, company=None):
        """
        Retrieve gender statistics data by production company.
        """
        self.logger.info("Retrieving gender statistics data by production company...")
        
        try:
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_company(company)
            
          return self.execute_aggregation_pipeline(pipeline)
        except Exception as e:
          self.logger.error(f"Error retrieving data by production company: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
    def get_gender_statistics_by_genre(self, genre=None):
        """
        Retrieve gender statistics data by movie genre.
        """
        self.logger.info("Retrieving gender statistics data by movie genre...")
        
        try:
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_genre(genre)
          
          return self.execute_aggregation_pipeline(pipeline)
        except Exception as e:
          self.logger.error(f"Error retrieving data by genre: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
    def get_gender_statistics_by_department(self, department=None):
        """
        Retrieve gender statistics data by department.
        """
        self.logger.info("Retrieving gender statistics data by department...")
        
        try:
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_department(department)
          
          return self.execute_aggregation_pipeline(pipeline)
        except Exception as e:
          self.logger.error(f"Error retrieving data by department: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
    def get_gender_statistics_by_year(self, year=None):
        """
        Retrieve gender statistics data by year.
        """
        self.logger.info("Retrieving gender statistics data by year...")
        
        try:
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_year(year)
          
          return self.execute_aggregation_pipeline(pipeline)
        except Exception as e:
          self.logger.error(f"Error retrieving data by year: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
    def execute_aggregation_pipeline(self, pipeline):
        """
        Execute the aggregation pipeline using the database repository.
        """
        self.logger.info("Executing aggregation pipeline...")
        
        try:
          cursor = self.gender_data_db_repo.execute_aggregation_pipeline(pipeline)
          
          result = list(cursor)
          
          self.logger.info(f"Aggregation pipeline result: {result}")
          
          return result
        except Exception as e:
          self.logger.error(f"Error executing aggregation pipeline: {e}")
          raise CustomError(GENDER_DATA_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
   
