from datetime import datetime
from utils.CustomErrors import CustomError
from utils.custom_status_codes import QUERY_CUSTOM_STATUS_CODES

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
      raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["missing_query"], 400)
    
    # Validate the query parameters
    if resource == 'movies':
      valid_fields = ['title', 'year', 'genre', 
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
          # Validate that actor is a valid string and not numeric
          if not isinstance(value, str) or value.isdigit():
            self.logger.error(f"Invalid actor name: {value}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_actor_value"], 400)

          # Search the credit db collection for the actor
          self.logger.info(f"Searching for movies with actor: {value}")
          
          actor_query = {
            "cast__elemMatch": {
                "name__icontains": value
            }
          }

          credits_for_actor = self.credit_db_repo.find_by_query(actor_query)
          
          if not credits_for_actor:
            self.logger.info(f"No movies found for actor {value}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[404]["no_movies_found"], 404)

          # Loop through credits_for_actor and retrieve the _id for all of the objects (movies the actor has acted in)
          movie_ids = [str(credit["id"]) for credit in credits_for_actor]
          self.logger.info(f"Movie IDs for actor {value}: {movie_ids}")
          
          query.update({'movie_id': {'$in': movie_ids}})
        elif field == 'rating':
          # Convert rating to a float
          try:
            value = float(value)
          except ValueError:
            self.logger.error(f"Invalid rating value: {value}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_rating_value"], 400)
          
          # Validate that rating is a valid number
          if not isinstance(value, (int, float)):
            self.logger.error(f"Invalid rating: {type(value)}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_rating_type"], 400)

          rating_threshold = float(value)

          if rating_threshold < 0 or rating_threshold > 5:
            self.logger.error(f"Invalid rating value: {rating_threshold}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_rating_value"], 400)
          
          ratings = []

          if resource == "rating":
            # Filtering ratings by their own value (direct rating filter)
            query["rating__gte"] = rating_threshold

          elif resource == "movie":
            # Validate that movie is a valid string
            if not isinstance(value, str):
              self.logger.error(f"Invalid movie: {type(value)}")
              raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_movie_value"], 400)
            
            # Filtering movies by rating (finding movies whose ratings meet the threshold)
            ratings_query = {"rating__gte": rating_threshold}
            ratings = self.rating_db_repo.find_by_query(ratings_query)
            
            if ratings:
              movie_ids = []

              for rating in ratings:
                try:
                  movie_ids.append(str(rating.movie_id))
                except Exception as e:
                  self.logger.warning(f"Invalid movie_id: {e}")
                
              query.update({"movie_id__in": movie_ids})
        elif field == 'genre':
          # Validate that genre is a valid string
          if not isinstance(value, str):
            self.logger.error(f"Invalid genre: {type(value)}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_genre_value"], 400)
          
          self.logger.info(f"Searching for movies with genre: {value}")

          query['genres__name__icontains'] = value
          
          movies_of_genre = self.movie_db_repo.find_by_query(query)
          # Loop through genres and retrieve the _id for all of the objects (movies with the genre)
          movie_ids = [movie.movie_id for movie in movies_of_genre]
          self.logger.info(f"Movie IDs for genre {value}: {movie_ids}")
          
          query.update({'movie_id': {'$in': movie_ids}})
        elif field == 'description':
          # Validate that description is a valid string
          if not isinstance(value, str):
            self.logger.error(f"Invalid description: {type(value)}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_description_value"], 400)
          
          self.logger.info(f"Searching for movies with description: {value}")
          
          query.update({'overview__icontains': value})        
        elif field == 'year':
          self.logger.info(f"Searching for movies with release year: {value}")

          # Search for movies by year, using datetime to create a date range (as suggested by copilot)
          year = int(value)

          if year < 1900 or year > datetime.now().year:
            self.logger.error(f"Invalid year: {year}")
            raise CustomError(QUERY_CUSTOM_STATUS_CODES[400]["invalid_year_value"], 400)

          start_date = datetime(year, 1, 1)
          end_date = datetime(year, 12, 31, 23, 59, 59)

          query.update({'release_date__gte': start_date, 'release_date__lte': end_date})
        else:
          # Search for movies by other fields
          self.logger.info(f"Searching for movies with {field}: {value}")

          query.update({f"{field}__icontains": value})

      return query
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Error occurred while building the query: {e}")
      raise CustomError(QUERY_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
