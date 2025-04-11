from flask import request, abort
from datetime import datetime

class MovieController:
  def __init__ (self, logger, movie_db_repo, credit_db_repo, rating_db_repo, generate_hateoas_links, json_convert, data_service):
    self.logger = logger
    self.json_convert = json_convert
    self.movie_db_repo = movie_db_repo
    self.credit_db_repo = credit_db_repo
    self.rating_db_repo = rating_db_repo
    self.generate_hateoas_links = generate_hateoas_links
    self.data_service = data_service
    
  def get_movies(self):
    self.logger.info("Fetching all movies")

    movies = self.movie_db_repo.find_all()

    if not movies:
      self.logger.info("No movies found")
      return {"message": "Not found"}, 404

    self.logger.info(f"Found {len(movies)} movies")
    
    movies_json = [
            {
                "id": str(movie.id),
                "movie_id": movie.movie_id,
                "title": movie.title,
                "release_year": movie.release_date.year if movie.release_date else None,
                "genre": [genre.name for genre in movie.genres],
                "description": movie.overview,
            }
            for movie in movies
        ]
    
    pagination_links = self.generate_hateoas_links.create_pagination_links("movie.get_movies", 1, 20, len(movies))
    self.logger.info("Pagination links generated")
  
    response = {
      "message": "Movies fetched successfully",
      "total": len(movies),
      "movies": movies_json,
      "_links": {
        **pagination_links
      }
    }, 200

    return response
  
  def get_movie_by_id(self, movie_id):
    self.logger.info(f"Fetching movie with ID: {movie_id}")

    movie = self.movie_db_repo.find_by_id(movie_id)

    if not movie:
      self.logger.info(f"Movie with ID {movie_id} not found")
      # return {"message": "Movie not found"}, 404
      abort(404)
    
    movie_links = self.generate_hateoas_links.create_movies_links(movie_id)

    movie_json = {
        "id": movie.movie_id,
        "title": movie.title,
        "release_year": movie.release_date.year if movie.release_date else None,
        "genre": [genre.name for genre in movie.genres],
        "description": movie.overview,
      }

    response = {
      "message": "Movie fetched successfully",
      "movie": movie_json,
      "_links": {
        "self": movie_links['self'],
        "delete": movie_links['delete'],
        "update": movie_links['update'],
        "actors": movie_links['actors'],
        "ratings": movie_links['ratings'],
      }
    }, 200

    return response
  
  def get_actors(self):
    self.logger.info("Fetching all actors")

    credits = self.credit_db_repo.find_all()

    if not credits:
      self.logger.info("No credits found")
      return {"message": "No actors found"}, 404

    actor_dict = {}

    # Extract actors from credits (as suggested by copilot)
    for credit in credits:
        movie = self.movie_db_repo.find_by_field('movie_id', credit.id)
        if not movie:
            continue
              
        for cast_member in credit.cast:
            if cast_member.id not in actor_dict:
                actor_dict[cast_member.id] = {
                    "id": cast_member.id,
                    "name": cast_member.name,
                    "movies_played": [],
                }
            actor_dict[cast_member.id]["movies_played"].append(movie.title)

        actors_json = list(actor_dict.values())

    pagination_links = self.generate_hateoas_links.create_pagination_links("movie.get_actors", 1, 20, len(actors_json))
    self.logger.info("Pagination links generated")

    response = {
      "message": "Actors fetched successfully",
      "total": len(actors_json),
      "actors": actors_json,
      "_links": {
        **pagination_links
      }
    }, 200

    return response

  def create_movie (self):
    """
    Handle client request to create a new movie.
    """
    self.logger.info("Adding new movie...")

    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      return {"message": "No data provided"}, 400

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    missing_fields = [field for field in required_fields if field not in movie_data]

    if missing_fields:
      self.logger.error(f"Missing required fields: {', '.join(missing_fields)}")
      return {"message": f"Missing required fields: {', '.join(missing_fields)}"}, 400

    try:
      movie_id = self.data_service.save_new_movie(movie_data)
      
      movie_links = self.generate_hateoas_links.create_movies_links(movie_id)
      
      response = {
        "message": "Movie added successfully",
        "_links": {
          "self": movie_links['self'],
          "delete": movie_links['delete'],
          "update": movie_links['update'],
          "actors": movie_links['credits'],
          "ratings": movie_links['ratings']
        }
      }, 201
      
      return response
    except Exception as e:
      self.logger.error(f"Error saving movie: {e}")
      return {"message": "Internal server error"}, 500  

  def delete_movie(self, movie_id):
    self.logger.info(f"Deleting movie with ID: {movie_id}")
    
    # Convert movie id to int since it's stored as an int in the ratings database
    movie_id_int = int(movie_id)
    
    try:
      # Check if the movie exists before deleting
      movie = self.movie_db_repo.find_by_id(movie_id_int)

      if not movie:
        self.logger.info(f"Movie with ID {movie_id} not found")
        return {"message": "Movie not found"}, 404

      # Delete associated ratings
      self.rating_db_repo.delete_by_field("movie_id", movie_id_int)
      self.logger.info(f"Ratings for movie with ID {movie_id} deleted successfully")

      # Delete the movie
      self.movie_db_repo.delete(movie_id)
      self.logger.info(f"Movie with ID {movie_id} deleted successfully")

      response = {
        "message": "Movie and associated ratings deleted successfully",
      }, 204

      return response
    except Exception as e:
      self.logger.error(f"Error deleting movie: {e}")
      return {"message": "Internal server error"}, 500
  
  def update_movie(self, movie_id):
    self.logger.info(f"Updating movie with ID: {movie_id}")

    # Get the movie data from the request body
    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      return {"message": "No data provided"}, 400

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    missing_fields = [field for field in required_fields if field not in movie_data]

    if missing_fields:
      self.logger.error(f"Missing required fields: {', '.join(missing_fields)}")
      return {"message": f"Missing required fields: {', '.join(missing_fields)}"}, 400

    try:
      # Update the movie data in the database
      self.movie_db_repo.update(movie_id, **movie_data)
      self.logger.info(f"Movie with ID {movie_id} updated successfully")
      
      movie_links = self.generate_hateoas_links.create_movies_links(movie_id)
      
      response = {
        "message": "Movie updated successfully",
        "_links": {
          "self": movie_links['self'],
          "delete": movie_links['delete'],
          "update": movie_links['update'],
          "actors": movie_links['credits'],
          "ratings": movie_links['ratings']
        }
      }, 200

      return response
    except Exception as e:
      self.logger.error(f"Error updating movie: {e}")
      return {"message": "Internal server error"}, 500

    