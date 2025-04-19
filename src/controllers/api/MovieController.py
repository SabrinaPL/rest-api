from flask import request, jsonify, make_response
from bson import ObjectId
from utils.CustomErrors import CustomError
from utils.custom_status_codes import MOVIE_CUSTOM_STATUS_CODES
from utils.validate import validate_fields

class MovieController:
  def __init__ (self, logger, movie_db_repo, credit_db_repo, rating_db_repo, generate_hateoas_links, json_convert, data_service, movie_query_service):
    self.logger = logger
    self.json_convert = json_convert
    self.movie_db_repo = movie_db_repo
    self.credit_db_repo = credit_db_repo
    self.rating_db_repo = rating_db_repo
    self.generate_hateoas_links = generate_hateoas_links
    self.data_service = data_service
    self.movie_query_service = movie_query_service
   
  # Helper methods to check if the movie has actors or ratings 
  def check_if_actors(self, movie_id):
    try:
        has_actors = bool(self.credit_db_repo.find_by_field("id", movie_id))
    except Exception as e:
        self.logger.error(f"Error checking actors for movie {movie_id}: {e}")
        has_actors = False

    return has_actors

  def check_if_ratings(self, movie_id):   
      try:
          # Movie id converted to int for querying the ratings collection
          movie_id_int = int(movie_id)
        
          has_ratings = bool(self.rating_db_repo.find_by_field("movie_id", movie_id_int))
      except Exception as e:
          self.logger.error(f"Error checking ratings for movie {movie_id}: {e}")
          has_ratings = False
        
      return has_ratings

  def get_movies(self):
    try:
      # Get potential query parameters from the request
      query_params = request.args.to_dict()
  
      # Extract and validate pagination parameters
      try:
        page = int(query_params.pop('page', 1))
        per_page = int(query_params.pop('per_page', 20))

        if page < 1 or per_page < 1:
          raise ValueError("Page and per_page must be greater than 0")
      except ValueError:
        self.logger.error("Invalid pagination parameters")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[400]["invalid_pagination"], 400)

      if query_params:
        self.logger.info("Query parameters provided, fetching movies by filter...")
      
        # Validate the query parameters
        query = self.movie_query_service.build_query('movies', query_params)
        self.logger.info("Query built successfully")
      else: 
        self.logger.info("Query parameters not provided, fetching all movies...")
        query = {}
     
      movies = self.movie_db_repo.find_by_query(query)

      if not movies:
        self.logger.info("No movies found")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)

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

      pagination_links = self.generate_hateoas_links.create_pagination_links("movie.get_movies", page, per_page, len(movies))
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
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Error fetching movies: {e}")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

  def get_movie_by_id(self, movie_id):
    try:
      self.logger.info(f"Fetching movie with ID: {movie_id}")
 
      # Validate and convert id to ObjectId
      try:
        movie_object_id = ObjectId(movie_id)
      except Exception as e:
        self.logger.error(f"Invalid ID format: {e}")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[400]["invalid_id"], 400)
    
      movie = self.movie_db_repo.find_by_id(movie_object_id)

      if not movie:
        self.logger.info(f"Movie with ID {movie_id} not found")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)
    
      # Query the credits and ratings collections using the string or int representation of movie_id
      has_actors = self.check_if_actors(movie.movie_id)
      has_ratings = self.check_if_ratings(movie.movie_id)

      movie_links = self.generate_hateoas_links.create_movies_links(movie_id, has_actors, has_ratings)

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
          "actors": movie_links['actors'] if has_actors else None,
          "ratings": movie_links['ratings'] if has_ratings else None,
        }
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Error fetching movie: {e}")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
  
  def create_movie (self):
    """
    Handle client request to create a new movie.
    """
    self.logger.info("Adding new movie...")

    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[400]["missing_data"], 400)

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    validate_fields(movie_data, required_fields)

    try:
      movie_id = self.data_service.save_new_movie(movie_data)
      
      movie_links = self.generate_hateoas_links.create_movies_links(movie_id, has_actors=False, has_ratings=False)
      
      response = {
        "message": "Movie added successfully",
        "_links": {
          "self": movie_links['self'],
          "delete": movie_links['delete'],
          "update": movie_links['update'],
        }
      }
      
      return make_response(jsonify(response), 201)
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Error saving movie: {e}")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

  def delete_movie(self, movie_id):
    self.logger.info(f"Deleting movie with ID: {movie_id}")

    try:
      # Check if the movie exists before deleting
      movie = self.movie_db_repo.find_by_id(movie_id)

      if not movie:
        self.logger.info(f"Movie with ID {movie_id} not found")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)

      try:
        # Delete the movie
        self.movie_db_repo.delete(movie_id)
        self.logger.info(f"Movie with ID {movie_id} deleted successfully")
      except Exception as e:
        self.logger.error(f"Error deleting movie: {e}")
        raise e

      response = {
        "message": "Movie deleted successfully",
      }

      return make_response(jsonify(response), 204)
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Error deleting movie: {e}")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
  
  def update_movie(self, movie_id):
    self.logger.info(f"Updating movie with ID: {movie_id}")

    # Get the movie data from the request body
    movie_data = request.get_json()

    if not movie_data:
      self.logger.error("No data provided in request body")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[400]["missing_data"], 400)

    # Validate required fields
    required_fields = ['title', 'release_date', 'genres']
    validate_fields(movie_data, required_fields)

    try:
      # Update the movie data in the database
      self.movie_db_repo.update(movie_id, **movie_data)
      self.logger.info(f"Movie with ID {movie_id} updated successfully")
      
      try:
        movie = self.movie_db_repo.find_by_id(movie_id)
      except Exception as e:
        self.logger.error(f"Error fetching updated movie: {e}")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
      
      if not movie:
        self.logger.info(f"Movie with ID {movie_id} not found")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)

      has_actors = self.check_if_actors(movie.movie_id)
      has_ratings = self.check_if_ratings(movie.movie_id)

      try:
        movie_links = self.generate_hateoas_links.create_movies_links(movie_id, has_actors, has_ratings)
      except Exception as e:
        self.logger.error(f"Error generating HATEOAS links: {e}")
        raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

      response = {
        "message": "Movie updated successfully",
        "_links": {
          "self": movie_links['self'],
          "delete": movie_links['delete'],
          "update": movie_links['update'],
          "actors": movie_links['actors'] if has_actors else None,
          "ratings": movie_links['ratings'] if has_ratings else None
        }
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.error(f"Custom error occurred: {e}")
      raise e
    except Exception as error:
      self.logger.error(f"Error updating movie: {error}")
      raise CustomError(MOVIE_CUSTOM_STATUS_CODES[500]["internal_error"], 500)


    