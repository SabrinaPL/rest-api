class AggregationPipelineService:
    def __init__(self, logger):
        self.logger = logger

    def gender_distribution_by_country(self, country=None):
        """
        Construct aggregation pipeline for gender data by country.
        If a country is provided, filter the data by that country, if not, return the pipeline for all countries.
        """
        self.logger.info("Constructing aggregation pipeline for gender data by production country...")

        match_stage = { 
           "countries": { "$exists": True },
           "gender": { "$in": [0, 1, 2] }
          }
 
        if country:
            # If a country is provided, filter the data by that country
            match_stage["countries"] = country

        return [
          # Use match to utilize the compound index on country and gender
          { "$match": match_stage },

          # Unwind the countries array to get individual country documents
          { "$unwind": "$countries" },
          
          # Match again after unwind if specific country was requested
          *([{ "$match": { "countries": country } }] if country else []),

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
          
          # Project the final output
          {
            "$project": {
              "country": "$_id",
              "total_count": "$total_count",
              "breakdown": {
                "$map": {
                  "input": "$breakdown",
                  "as": "item",
                  "in": {
                    "gender": "$$item.gender",
                    "count": "$$item.count",
                    "percentage": {
                      "$multiply": [
                        { "$divide": ["$$item.count", "$total_count"] },
                        100
                      ]
                    }
                  }
                }
              }
            }
          }
        ]
 
    def gender_distribution_by_company(self, company=None):

        """
        Construct aggregation pipeline for gender data by company.
        If a company is provided, filter the data by that company, if not, return the pipeline for all companies.
        """
        self.logger.info("Constructing aggregetion pipeline for gender data by company...")
        
        match_stage = {
           "companies": { "$exists": True },
           "gender": { "$in": [0, 1, 2] }
        }
        
        if company:
            # If a company is provided, filter the data by that company
            match_stage["companies"] = company
        
        return [
          # Use match to utilize the compound index on company
          { "$match": match_stage },
          
          # Unwind the companies array to get individual company documents
          { "$unwind": "$companies" },
          
          # Match again after unwind if specific company was requested
          *([{ "$match": { "companies": company } }] if company else []),
          
          # Group by company and gender to count occurrences
          {
            "$group": {
              "_id": 
                { 
                 "company": "$companies",
                 "gender": "$gender"
                },
              "count": { "$sum": 1 }
            }
          },
          
          # Regroup by company to get total counts
          {
            "$group": {
              "_id": "$_id.company",
              "total_count": { "$sum": "$count" },
              "breakdown": {
                "$push": {
                  "gender": "$_id.gender",
                  "count": "$count"
                }
              }
            }
          },
          
          # Project the final output
          {
            "$project": {
              "company": "$_id",
              "total_count": "$total_count",
              "breakdown": {
                "$map": {
                  "input": "$breakdown",
                  "as": "item",
                  "in": {
                    "gender": "$$item.gender",
                    "count": "$$item.count",
                    "percentage": {
                      "$multiply": [
                        { "$divide": ["$$item.count", "$total_count"] },
                        100
                      ]
                    }
                  }
                }
              }
            }
          }
        ]
        
    def gender_distribution_by_genre(self, genre=None):
        """
        Construct aggregation pipeline for gender data by movie genre.
        If a genre is provided, filter the data by that genre, if not, return the pipeline for all genres.
        """
        self.logger.info("Retrieving aggregation pipeline for gender data by genre...")
        
        match_stage = {
           "genres": { "$exists": True },
           "gender": { "$in": [0, 1, 2] }
        }
        
        if genre:
            # If a genre is provided, filter the data by that genre
            match_stage["genres"] = genre
       
        
        return [
          # Use match to utilize the compound index on genre
          { "$match": match_stage },
          
          # Unwind the genres array to get individual genre documents
          { "$unwind": "$genres" },
          
          # Match again after unwind if specific genre was requested
          *([{ "$match": { "genres": genre } }] if genre else []),
          
          # Group by genre and gender to count occurrences
          {
            "$group": {
              "_id": 
                { 
                 "genre": "$genres",
                 "gender": "$gender"
                },
              "count": { "$sum": 1 }
            }
          },
          
          # Regroup by genre to get total counts
          {
            "$group": {
              "_id": "$_id.genre",
              "total_count": { "$sum": "$count" },
              "breakdown": {
                "$push": {
                  "gender": "$_id.gender",
                  "count": "$count"
                }
              }
            }
          },
          
          # Project the final output
          {
            "$project": {
              "genre": "$_id",
              "total_count": "$total_count",
              "breakdown": {
                "$map": {
                  "input": "$breakdown",
                  "as": "item",
                  "in": {
                    "gender": "$$item.gender",
                    "count": "$$item.count",
                    "percentage": {
                      "$multiply": [
                        { "$divide": ["$$item.count", "$total_count"] },
                        100
                      ]
                    }
                  }
                }
              }
            }
          }
        ]
    
    def gender_distribution_by_department(self, department=None):
        """
        Construct aggregation pipeline for gender data by department.
        If a department is provided, filter the data by that department, if not, return the pipeline for all departments.
        """
        self.logger.info("Retrieving aggregation pipeline for gender data by department...")
      
        match_stage = {
           "department": { "$exists": True },
           "gender": { "$in": [0, 1, 2] }
        }
        
        if department:
            # If a department is provided, filter the data by that department
            match_stage["department"] = department

        return [
          { "$match": match_stage },
          
          # Group by department and gender to count occurrences
          {
            "$group": {
              "_id": 
                { 
                 "department": "$department",
                 "gender": "$gender"
                },
              "count": { "$sum": 1 }
            }
            
          # Regroup by department to get total counts
          },
          {
            "$group": {
              "_id": "$_id.department",
              "total_count": { "$sum": "$count" },
              "breakdown": {
                "$push": {
                  "gender": "$_id.gender",
                  "count": "$count"
                }
              }
            }
            
          # Project the final output
          },
          {
            "$project": {
              "department": "$_id", 
              "total_count": 1,
              "breakdown": {
                "$map": {
                  "input": "$breakdown",
                  "as": "item",
                  "in": {
                    "gender": "$$item.gender",
                    "count": "$$item.count",
                    "percentage": {
                      "$multiply": [
                        { "$divide": ["$$item.count", "$total_count"] },
                        100
                      ]
                    }
                  }
                }
              }
            }
          }
        ]
    
    def gender_distribution_by_year(self, year=None):
        """
        Construct aggregation pipeline for gender data by year.
        If a year is provided, filter the data by that year, if not, return the pipeline for all years.
        """
        self.logger.info("Retrieving aggregation pipeline for gender data by year...")
        
        match_stage = {
           "year": { "$exists": True },
           "gender": { "$in": [0, 1, 2] }
        }
        
        if year:
            # If a year is provided, filter the data by that year
            match_stage["year"] = year
        
        return [
          { "$match": match_stage },
          
          # Group by year and gender to count occurrences
          {
            "$group": {
              "_id": 
                { 
                 "year": "$year",
                 "gender": "$gender"
                },
              "count": { "$sum": 1 }
            }
            
          # Regroup by year to get total counts
          },
          {
            "$group": {
              "_id": "$_id.year",
              "total_count": { "$sum": "$count" },
              "breakdown": {
                "$push": {
                  "gender": "$_id.gender",
                  "count": "$count"
                }
              }
            }
            
          # Project the final output
          },
          {
            "$project": {
              "year": "$_id", 
              "total_count": 1,
              "breakdown": {
                "$map": {
                  "input": "$breakdown",
                  "as": "item",
                  "in": {
                    "gender": "$$item.gender",
                    "count": "$$item.count",
                    "percentage": {
                      "$multiply": [
                        { "$divide": ["$$item.count", "$total_count"] },
                        100
                      ]
                    }
                  }
                }
              }
            }
          }
        ]