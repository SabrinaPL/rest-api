class GenderDataQueryService:
    def __init__(self, logger, gender_data_db_repo, aggregation_pipeline_service):
      self.logger = logger
      self.gender_data_db_repo = gender_data_db_repo
      self.aggregation_pipeline_service = aggregation_pipeline_service

    # def build_query(self, resource, query_params):
    #   self.logger.info(f"Searching for {resource} with query parameters {query_params}...")

    # TODO: this class will be responsible for calling the GenderDataAggregations class to retrieve the aggregation pipelines to pass on to the db repo (db wrapper class) which in turn will call the db client to execute the aggregation pipeline and return the results. This class will also build queries for filtering