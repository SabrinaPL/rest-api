from flask import request, jsonify, make_response
from utils.CustomErrors import CustomError
from utils.validate import validate_fields

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
      raise CustomError("Not found", 404)

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
    }

    return make_response(jsonify(response), 200)
  
  def get_movie_by_id(self, movie_id):
    self.logger.info(f"Fetching movie with ID: {movie_id}")

    movie = self.movie_db_repo.find_by_id(movie_id)

    if not movie:
      self.logger.info(f"Movie with ID {movie_id} not found")
      raise CustomError("Not found", 404)
    
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
    }

    return make_response(jsonify(response), 200)
  
  def create_movie (self):
    """
    Handle client request to create a new movie.
    """
    self.logger.info("Adding new movie...")

    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      raise CustomError("No data provided", 400)

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    validate_fields(movie_data, required_fields)

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
      }
      
      return make_response(jsonify(response), 201)
    except Exception as e:
      self.logger.error(f"Error saving movie: {e}")
      raise CustomError("Internal server error", 500)

  def delete_movie(self, movie_id):
    self.logger.info(f"Deleting movie with ID: {movie_id}")
    
    # Convert movie id to int since it's stored as an int in the ratings database
    movie_id_int = int(movie_id)
    
    try:
      # Check if the movie exists before deleting
      movie = self.movie_db_repo.find_by_id(movie_id_int)

      if not movie:
        self.logger.info(f"Movie with ID {movie_id} not found")
        raise CustomError("Not found", 404)

      # Delete associated ratings
      self.rating_db_repo.delete_by_field("movie_id", movie_id_int)
      self.logger.info(f"Ratings for movie with ID {movie_id} deleted successfully")

      # Delete the movie
      self.movie_db_repo.delete(movie_id)
      self.logger.info(f"Movie with ID {movie_id} deleted successfully")

      response = {
        "message": "Movie and associated ratings deleted successfully",
      }

      return make_response(jsonify(response), 204)
    except Exception as e:
      self.logger.error(f"Error deleting movie: {e}")
      raise CustomError("Internal server error", 500)
  
  def update_movie(self, movie_id):
    self.logger.info(f"Updating movie with ID: {movie_id}")

    # Get the movie data from the request body
    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      raise CustomError("No data provided", 400)

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    validate_fields(movie_data, required_fields)

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
      }

      return make_response(jsonify(response), 200)
    except Exception as e:
      self.logger.error(f"Error updating movie: {e}")
      raise CustomError("Internal server error", 500)

    