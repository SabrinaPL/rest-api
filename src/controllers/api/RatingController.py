
from flask import jsonify, make_response, request
from utils.CustomErrors import CustomError 
from utils.custom_status_codes import RATING_CUSTOM_STATUS_CODES
from bson import ObjectId

class RatingController:
  def __init__(self, logger, rating_db_repo, movie_db_repo, json_convert, generate_hateoas_links, movie_query_service):
    self.rating_db_repo = rating_db_repo
    self.movie_db_repo = movie_db_repo
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.movie_query_service = movie_query_service
    self.logger = logger
 
  def get_ratings(self):
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
        raise CustomError(RATING_CUSTOM_STATUS_CODES[400]["invalid_pagination"], 400)
    
      if query_params:
        self.logger.info("Query parameter provided, fetching ratings by filter...")

        # Validate the query parameters
        query = self.movie_query_service.build_query('rating', query_params)
        self.logger.info("Query built successfully")
      else:
        self.logger.info("Query parameters not provided, fetching all ratings...")
        query = {}

      self.logger.info(f"Fetching ratings with query: {query}")
      
      try:
        ratings = self.rating_db_repo.find_by_query(query)
      except Exception as e:
        self.logger.error(f"Error fetching ratings: {e}")
        raise e
      
      if not ratings:
        self.logger.info("No ratings found")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[404]["no_ratings"], 404)

      try:
        # Convert ratings to JSON format
        self.json_convert.serialize_documents(ratings)
        self.logger.info("Ratings converted to JSON format")
      except Exception as e:
        self.logger.error(f"Error converting ratings to JSON format: {e}")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

      processed_ratings = []

      for rating in ratings:
        try:
          rating_id = str(rating.id)
          movie_id = str(rating.movie_id)
  
          movie = self.movie_db_repo.find_by_field("movie_id", movie_id)
          movie_title = movie.title if movie else "Unknown"

          processed_ratings.append({
              "id": rating_id,
              "text": f"{rating['rating']}/5",
              "movie": movie_title
          })
        except Exception as e:
          self.logger.error(f"Error processing rating: {e}")
          raise e

      try:
        pagination_links = self.generate_hateoas_links.create_pagination_links("rating.get_ratings", page, per_page, len(ratings))
        self.logger.info("Pagination links generated")
      except Exception as e:
        self.logger.error(f"Error generating pagination links: {e}")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

      response = {
              "message": "Ratings fetched successfully",
              "total": len(ratings),
              "ratings": processed_ratings,
              "_links": {
                  **pagination_links
              }
          }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.info(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Unexpected error while fetching ratings: {e}")
      raise e

  def get_movie_rating(self, _id):
    try:
      self.logger.info(f"Fetching ratings for movie with ID: {_id}")

      # Validate and convert id to ObjectId
      try:
        _id = ObjectId(_id)
      except Exception as e:
        self.logger.error(f"Invalid ID format: {e}")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[400]["invalid_id"], 400)
    
      # Fetch the movie from the db to retrieve the movie_id
      movie = self.movie_db_repo.find_by_id(_id)

      if not movie:
        self.logger.info(f"No movie found with ID {_id}")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)

      # Convert movie id to int since it's stored as an int in the ratings database collection
      movie_id = int(movie.movie_id)

      ratings = self.rating_db_repo.find_all_by_field("movie_id", movie_id)

      if not ratings or len(ratings) == 0:
        self.logger.info(f"No ratings found for movie with ID {movie_id}")
        raise CustomError(RATING_CUSTOM_STATUS_CODES[404]["no_ratings"], 404)
      
      # Process ratings to extract relevant information
      processed_ratings = []
      for rating in ratings:
        try:
          processed_ratings.append({
            "id": str(rating.id),
            "user_id": str(rating.user_id),
            "movie_title": movie.title,
            "rating": rating.rating
          })

        except Exception as e:
          self.logger.error(f"Error processing rating: {e}")
          raise CustomError(RATING_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
 
      movie_links = self.generate_hateoas_links.create_movies_links(_id, has_actors=False, has_ratings=bool(ratings))

      response = {
        "message": "Ratings fetched successfully",
        "total": len(processed_ratings),
        "ratings": processed_ratings,
        "_links": {
          "self": movie_links['ratings'],
          "movie": movie_links['self']
        }
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.info(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Unexpected error while fetching ratings: {e}")
      raise e
  