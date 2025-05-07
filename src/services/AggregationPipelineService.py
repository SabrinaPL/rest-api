class AggregationPipelineService:
    def __init__(self, logger):
        self.logger = logger
    def gender_distribution_by_country(self):
        """
        Construct aggregation pipeline for gender data by country.
        """
        self.logger.info("Aggregating gender data by country...")
        
        pipeline = [
          # Unwind the countries array to get individual country documents
          { "$unwind": "$countries" },
          
          # Group by country and gender to count occurrences
          {
            "$group": {
              "_id": 
                { 
                 "country": "$countries", 
                 "gender": "$gender" 
                 },
              "count": { "$sum": 1 }
            }
          },
          
          # Regroup by country to get total counts
          {
            "$group": {
              "_id": "$_id.country",
              "total_count": { "$sum": "$count" },
              "breakdown": {
                "$push": {
                  "gender": "$_id.gender",
                  "count": "$count"
                }
              }
            }
          },
          
          # Unwind the breakdown array to calculate percentages (as suggested by chatGPT)
          { "$unwind": "$breakdown" },
          
          {
            "$project": {
              "country": "$_id",
              "gender": "$breakdown.gender",
              "count": "$breakdown.count",
              "percentage": {
                "$multiply": [
                  { "$divide": ["$breakdown.count", "$total_count"] },
                  100
                ]
              }
            }
          }
        ]
        
        return pipeline
        
    def gender_distribution_by_company(self):
        """
        Construct aggregation pipeline for gender data by company.
        """
        self.logger.info("Aggregating gender data by company...")
        
        pipeline = [
          
        ]
        
    def gender_distribution_by_genre(self):
        """
        Construct aggregation pipeline for gender data by movie genre.
        """
        self.logger.info("Aggregating gender data by genre...")
        
        pipeline = [
          
        ]
        
    def gender_distribution_by_department(self):
        """
        Construct aggregation pipeline for gender data by department.
        """
        self.logger.info("Aggregating gender data by department...")
        
        pipeline = [
          
        ]
        
    def gender_distribution_by_year(self):
        """
        Construct aggregation pipeline for gender data by year.
        """
        self.logger.info("Aggregating gender data by year...")
        
        pipeline = [
          
        ]