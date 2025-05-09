class GenderStatisticsService:
    def __init__(self, logger, gender_data_db_repo, aggregation_pipeline_service):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.aggregation_pipeline_service = aggregation_pipeline_service

    def get_gender_statistics_by_country(self, country=None):
        """
        Retrieve gender statistics data by country.
        """
        self.logger.info("Retrieving gender statistics data by country...")

        try:
          # Call the aggregation pipeline service to get the pipeline
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_country(country)
        
          # Execute the aggregation pipeline using the db repo
          cursor = self.gender_data_db_repo.execute_aggregation_pipeline(pipeline)
          
          result = list(cursor)
          
          self.logger.info(f"Aggregation pipeline result: {result}")
          return result 
        except Exception as e:
          self.logger.error(f"Error retrieving data by country: {e}")
          raise e
   
    def get_gender_statistics_by_company(self, company=None):
        """
        Retrieve gender statistics data by production company.
        """
        self.logger.info("Retrieving gender statistics data by production company...")
        
        try:
          pipeline = self.aggregation_pipeline_service.gender_distribution_by_company(company)
          
          cursor = self.gender_data_db_repo.execute_aggregation_pipeline(pipeline)
          
          result = list(cursor)
          
          self.logger.info(f"Aggregation pipeline result: {result}")
          return result
        except Exception as e:
          self.logger.error(f"Error retrieving data by production company: {e}")
          raise e
