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
    
    movies_json = [
            {
                "id": movie.movie_id,
                "title": movie.title,
                "release_year": movie.release_date.year if movie.release_date else None,
                "genre": [genre.name for genre in movie.genres],
                "description": movie.overview,
            }
            for movie in movies
        ]

    # TODO: Fix hateoas links
    response = {
      "message": "Movies fetched successfully",
      "total": len(movies),
      "movies": movies_json,
      "_links": {
        "self": "/api/v1/movies",
        "create": "/api/v1/movies",
        "update": "/api/v1/movies/{id}",
        "delete": "/api/v1/movies/{id}",
        "search": "/api/v1/movies/search",
        "first": "/api/v1/movies?page=1",
        "next": f"/api/v1/movies?page=2" if len(movies) > 20 else None,
        "last": f"/api/v1/movies?page={len(movies) // 20}"
      }
    }

    return response, 200
  
  def get_movie_by_id(self, movie_id):
    self.logger.info(f"Fetching movie with ID: {movie_id}")

    movie = self.movie_db_repo.find_by_id(movie_id)

    if not movie:
      self.logger.info(f"Movie with ID {movie_id} not found")
      return {"message": "Movie not found"}, 404

    movie_json = {
        "id": movie.movie_id,
        "title": movie.title,
        "release_year": movie.release_date.year if movie.release_date else None,
        "genre": [genre.name for genre in movie.genres],
        "description": movie.overview,
      }

    # TODO: Fix hateoas links
    response = {
      "message": "Movie fetched successfully",
      "movie": movie_json,
      "_links": {
        "self": f"/api/v1/movies/{movie_id}",
        "update": f"/api/v1/movies/{movie_id}",
        "delete": f"/api/v1/movies/{movie_id}",
        "credits": f"/api/v1/movies/{movie_id}/credits",
        "ratings": f"/api/v1/movies/{movie_id}/ratings"
      }
    }

    return response, 200
  
  def get_actors(self):
    self.logger.info("Fetching all actors")

    credits = self.credit_db_repo.find_all()

    if not credits:
      self.logger.info("No credits found")
      return {"message": "No actors found"}, 404
    
    # Extract all actors from credits
    actors = []
    for credit in credits:
      actors.extend(credit.cast) # Extracting cast from each credit
    if not actors:
      self.logger.info("No actors found")
      return {"message": "No actors found"}, 404
    
    # Convert actors to JSON format
    actors_json = self.json_convert.serialize_documents(actors)
    self.logger.info("Actors converted to JSON format")

    # TODO: Fix hateoas links
    response = {
      "message": "Actors fetched successfully",
      "total": len(actors),
      "actors": actors_json,
      "_links": {
        "self": "/api/v1/actors",
        "movie credits": "/api/v1/movies/{movie_id}/credits",
        "movie ratings": "/api/v1/movies/{movie_id}/ratings",
        "ratings": "/api/v1/ratings",
        "search": "/api/v1/actors/search",
        "first": "/api/v1/actors?page=1",
        "next": f"/api/v1/actors?page=2" if len(actors) > 10 else None,
        "last": f"/api/v1/actors?page={len(actors) // 10}"
      }
    }

    return response, 200
  
  def get_ratings(self):
    self.logger.info("Fetching all ratings")

    ratings = self.rating_db_repo.find_all()

    if not ratings:
      self.logger.info("No ratings found")
      return {"message": "No ratings found"}, 404
    
    # Convert ratings to JSON format
    ratings_json = self.json_convert.serialize_documents(ratings)
    self.logger.info("Ratings converted to JSON format")

    # TODO: Fix hateoas links
    
    response = {
      "message": "Ratings fetched successfully",
      "total": len(ratings),
      "ratings": ratings_json,
      "_links": {
        "self": "/api/v1/ratings",
        "movies": "/api/v1/movies/{movie_id}",
        "movie credits": "/api/v1/movies/{movie_id}/credits",
        "movie ratings": "/api/v1/movies/{movie_id}/ratings",
        "actors": "/api/v1/actors/",
        "first": "/api/v1/ratings?page=1",
        "next": f"/api/v1/ratings?page=2" if len(ratings) > 20 else None,
        "last": f"/api/v1/ratings?page={len(ratings) // 20}"
      }
    }

    return response, 200

  def get_actors_by_movie(self, movie_id):
    self.logger.info(f"Fetching actors for movie with ID: {movie_id}")

    credits = self.credit_db_repo.find_by_id(movie_id)

    if not credits:
      self.logger.info(f"No actors found for movie with ID {movie_id}")
      return {"message": "No actors found for this movie"}, 404

    # Extract all actors from credits
    actors = []
    if hasattr(credits, 'cast'):
      for credit in credits.cast:
        actors.append(credit)
        
    if not actors:
      self.logger.info(f"No actors found for movie with ID {movie_id}")
      return {"message": "No actors found for this movie"}, 404

    # Convert actors to JSON format
    actors_json = self.json_convert.serialize_documents(actors)
    self.logger.info("Actors converted to JSON format")
    
    # TODO: Fix hateoas links

    response = {
      "message": "Actors fetched successfully",
      "total": len(actors),
      "actors": actors_json,
      "_links": {
        "self": f"/api/v1/movies/{movie_id}/credits",
        "movies": "/api/v1/movies",
        "movie ratings": f"/api/v1/movies/{movie_id}/ratings",
        "ratings": "/api/v1/ratings",
        "first": f"/api/v1/movies/{movie_id}/credits?page=1",
        "next": f"/api/v1/movies/{movie_id}/credits?page=2" if len(actors) > 10 else None,
        "last": f"/api/v1/movies/{movie_id}/credits?page={len(actors) // 10}"
      }
    }
    return response, 200
    