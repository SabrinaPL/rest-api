class MovieController:
  def __init__ (self, logger, movie_db_repo, credit_db_repo, rating_db_repo, json_convert):
    self.logger = logger
    self.movie_db_repo = movie_db_repo
    self.credit_db_repo = credit_db_repo
    self.rating_db_repo = rating_db_repo
    self.json_convert = json_convert
    
  def get_movies(self):
    self.logger.info("Fetching all movies")

    movies = self.movie_db_repo.find_all()
    if not movies:
      self.logger.info("No movies found")
      return {"message": "No movies found"}, 404
    self.logger.info(f"Found {len(movies)} movies")
    
    # Convert movies to JSON format
    movies_json = self.json_convert.serialize_documents(movies)
    self.logger.info("Movies converted to JSON format")
    
    return movies_json, 200