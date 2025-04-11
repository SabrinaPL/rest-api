from datetime import datetime

# Service class used to query movies from the database by parameters
class MovieQueryService:
  def __init__(self, logger, movie_db_repo, credit_db_repo, rating_db_repo):
    self.logger = logger
    self.movie_db_repo = movie_db_repo
    self.credit_db_repo = credit_db_repo
    self.rating_db_repo = rating_db_repo
  
  def build_query(self, query_params):
    self.logger.info("Searching for movies with query parameters...")
    
    # Retrieve all query parameters
    # query_params = request.args.to_dict()

    if not query_params:
      self.logger.info("No query parameters provided")
      return {"message": "No query parameters provided"}, 400
    
    self.logger.info(f"Query parameters: {query_params}")
    
    # Validate the query parameters
    valid_fields = ['movie_id', 'title', 'year', 'genre', 
                    'actor', 'description', 'rating']
    invalid_fields = [field for field in query_params if field not in valid_fields]
    
    if invalid_fields:
      self.logger.error(f"Invalid query parameters: {', '.join(invalid_fields)}")
      return {"message": f"Invalid query parameters: {', '.join(invalid_fields)}"}, 400
    
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
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'rating':
          self.logger.info(f"Searching for movies with rating: {value}")
          
          query['rating__gte'] = float(value)
          if query['rating__gte'] < 0 or query['rating__gte'] > 5:
            self.logger.error(f"Invalid rating: {query['rating__gte']}")
            return {"message": "Invalid rating"}, 400
          
          movies_by_rating = self.rating_db_repo.find_by_query(query)
          # Loop through ratings and retrieve the _id for all of the objects (movies with the rating)
          movie_ids = [str(rating.movie_id) for rating in movies_by_rating]
          
          self.logger.info(f"Movie IDs for rating {value}: {movie_ids}")
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'genre':
          self.logger.info(f"Searching for movies with genre: {value}")

          query['genres__name__icontains'] = value
          
          movies_of_genre = self.movie_db_repo.find_by_query(query)
          # Loop through genres and retrieve the _id for all of the objects (movies with the genre)
          movie_ids = [movie.movie_id for movie in movies_of_genre]
          self.logger.info(f"Movie IDs for genre {value}: {movie_ids}")
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'description':
          self.logger.info(f"Searching for movies with description: {value}")
          
          query['overview__icontains'] = value        
        elif field == 'year':
          self.logger.info(f"Searching for movies with release year: {value}")

          # Search for movies by year, using datetime to create a date range (as suggested by copilot)
          year = int(value)
          if year < 1900 or year > datetime.now().year:
            self.logger.error(f"Invalid year: {year}")
            return {"message": "Invalid year"}, 400

          start_date = datetime(year, 1, 1)
          end_date = datetime(year, 12, 31, 23, 59, 59)
          query['release_date__gte'] = start_date
          query['release_date__lte'] = end_date
        else:
          # Search for movies by other fields
          self.logger.info(f"Searching for movies with {field}: {value}")

          query[f"{field}__icontains"] = value
      
      # Query the movie database for the movies
      # self.logger.info(f"Querying movies with filters: {query}")
      # movies = self.movie_db_repo.find_by_query(query)
      
      # if not movies:
      #  self.logger.info("No movies found with the given filters")
      #  return {"message": "Not found"}, 404

      # movies_json = [
      #     {
      #         "id": movie.movie_id,
      #         "title": movie.title,
      #         "release_year": movie.release_date.year if movie.release_date else None,
      #         "genre": [genre.name for genre in movie.genres],
      #         "description": movie.overview,
      #     }
      #     for movie in movies
      # ]
      
      # pagination_links = self.generate_hateoas_links.create_pagination_links("movie.search_movie", 1, 20, len(movies))
      # self.logger.info("Pagination links generated")
 
      # response = {
      #   "message": "Movies fetched successfully",
      #   "total": len(movies),
      #   "movies": movies_json,
      #   "_links": {
      #     "self": f"/api/v1/movies/search?{query}",
      #     **pagination_links
      #   }
      # }, 200

      return query 
    
    except Exception as e:
      self.logger.error(f"Error occurred while building the query: {e}")
      return {"message": "Internal server error"}, 500
