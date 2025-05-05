class GenderDataQueryService:
    def __init__(self, logger, gender_data_db_repo):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo

    # def build_query(self, resource, query_params):
    #   self.logger.info(f"Searching for {resource} with query parameters {query_params}...")
