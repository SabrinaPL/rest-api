from datetime import datetime
from utils.CustomErrors import CustomError

# Service class used to query movies from the database by parameters
class MovieQueryService:
  def __init__(self, logger, movie_db_repo, credit_db_repo, rating_db_repo):
    self.logger = logger
    self.movie_db_repo = movie_db_repo
    self.credit_db_repo = credit_db_repo
    self.rating_db_repo = rating_db_repo
  
  def build_query(self, resource, query_params):
    self.logger.info(f"Searching for movies with query parameters {query_params}...")

    if not query_params:
      self.logger.info("No query parameters provided")
      return {"message": "No query parameters provided"}, 400
    
    # Validate the query parameters
    if resource == 'movies':
      valid_fields = ['movie_id', 'title', 'year', 'genre', 
                    'actor', 'description', 'rating']
    elif resource == 'actors':
      valid_fields = ['actor']
    elif resource == 'ratings':
      valid_fields = ['rating']
  
    invalid_fields = [field for field in query_params if field not in valid_fields]
    
    if invalid_fields:
      self.logger.error(f"Invalid query parameters: {', '.join(invalid_fields)}")
      raise ValueError(f"Invalid query parameters: {', '.join(invalid_fields)}")
    
    try:
      query = {}
      
      for field, value in query_params.items():
        if field == 'actor':
          # Search the credit db collection for the actor
          self.logger.info(f"Searching for movies with actor: {value}")
          
          query['cast__name__icontains'] = value
          credits_for_actor = self.credit_db_repo.find_by_query(query)
          
          # Loop through credits_for_actor and retrieve the _id for all of the objects (movies the actor has acted in)
          movie_ids = [credit.id for credit in credits_for_actor]
          self.logger.info(f"Movie IDs for actor {value}: {movie_ids}")
          
          query.update({'id': {'$in': movie_ids}})
        elif field == 'rating':
          self.logger.info(f"Searching for movies with rating: {value}")
          
          query['rating__gte'] = float(value)
          if query['rating__gte'] < 0 or query['rating__gte'] > 5:
            self.logger.error(f"Invalid rating: {query['rating__gte']}")
            raise CustomError("Invalid filter value", 400)

          movies_by_rating = self.rating_db_repo.find_by_query(query)
          # Loop through ratings and retrieve the _id for all of the objects (movies with the rating)
          movie_ids = [str(rating.movie_id) for rating in movies_by_rating]
          
          self.logger.info(f"Movie IDs for rating {value}: {movie_ids}")
          
          query.update({'movie_id': {'$in': movie_ids}})
        elif field == 'genre':
          self.logger.info(f"Searching for movies with genre: {value}")

          query['genres__name__icontains'] = value
          
          movies_of_genre = self.movie_db_repo.find_by_query(query)
          # Loop through genres and retrieve the _id for all of the objects (movies with the genre)
          movie_ids = [movie.movie_id for movie in movies_of_genre]
          self.logger.info(f"Movie IDs for genre {value}: {movie_ids}")
          
          query.update({'movie_id': {'$in': movie_ids}})
        elif field == 'description':
          self.logger.info(f"Searching for movies with description: {value}")
          
          query.update({'overview__icontains': value})        
        elif field == 'year':
          self.logger.info(f"Searching for movies with release year: {value}")

          # Search for movies by year, using datetime to create a date range (as suggested by copilot)
          year = int(value)

          if year < 1900 or year > datetime.now().year:
            self.logger.error(f"Invalid year: {year}")
            raise CustomError("Invalid filter value", 400)

          start_date = datetime(year, 1, 1)
          end_date = datetime(year, 12, 31, 23, 59, 59)

          query.update({'release_date__gte': start_date, 'release_date__lte': end_date})
        else:
          # Search for movies by other fields
          self.logger.info(f"Searching for movies with {field}: {value}")

          query.update({f"{field}__icontains": value})

      return query
    
    except Exception as e:
      self.logger.error(f"Error occurred while building the query: {e}")
      raise CustomError("Internal server error", 500)
