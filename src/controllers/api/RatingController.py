
from flask import jsonify, make_response, request
from utils.CustomErrors import CustomError 

class RatingController:
  def __init__(self, logger, rating_db_repo, movie_db_repo, json_convert, generate_hateoas_links, movie_query_service):
    self.rating_db_repo = rating_db_repo
    self.movie_db_repo = movie_db_repo
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.movie_query_service = movie_query_service
    self.logger = logger
 
  def get_ratings(self):
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
      raise CustomError("Invalid pagination parameters", 400)
    
    if query_params:
      self.logger.info("Query parameters provided, fetching ratings by filter...")
      
      # Validate the query parameters
      query = self.movie_query_service.build_query(query_params)
      self.logger.info("Query built successfully")
    else:
      self.logger.info("Query parameters not provided, fetching all ratings...")
      query = {}
    
    ratings = self.rating_db_repo.find_by_query(query)

    if not ratings:
      self.logger.info("No ratings found")
      raise CustomError("Not found", 404)

    ratings_json = self.json_convert.serialize_documents(ratings)
    self.logger.info("Ratings converted to JSON format")

    # Process ratings and convert them to JSON format
    processed_ratings = []

    for rating in ratings_json:
        rating_id = str(rating["_id"]["$oid"])
        
        movie_id = str(rating["movie_id"])

        movie = self.movie_db_repo.find_by_field("movie_id", movie_id)
        movie_title = movie.title if movie else "Unknown"

        processed_ratings.append({
            "id": rating_id,
            "text": f"{rating['rating']}/5",
            "movie": movie_title
        })
        
        pagination_links = self.generate_hateoas_links.create_pagination_links("rating.get_ratings", page, per_page, len(ratings_json))
        self.logger.info("Pagination links generated")

    response = {
            "message": "Ratings fetched successfully",
            "total": len(ratings),
            "ratings": processed_ratings,
            "_links": {
                **pagination_links
            }
        }

    return make_response(jsonify(response), 200)

  def get_movie_rating(self, movie_id):
    self.logger.info(f"Fetching ratings for movie with ID: {movie_id}")

    # Convert movie id to int since it's stored as an int in the ratings database collection
    movie_id_int = int(movie_id)

    ratings = self.rating_db_repo.find_by_field("movie_id", movie_id_int)

    if not ratings:
      self.logger.info(f"No ratings found for movie with ID {movie_id}")
      raise CustomError("Not found", 404)

    # Convert ratings to JSON format
    ratings_json = self.json_convert.serialize_documents(ratings)
    self.logger.info("Ratings converted to JSON format")
    
    movie_links = self.generate_hateoas_links.create_movies_links(movie_id)
    pagination_links = self.generate_hateoas_links.create_pagination_links("rating.get_ratings_by_movie", 1, 20, len(ratings_json), movie_id=movie_id)
    self.logger.info("Pagination links generated")

    response = {
      "message": "Ratings fetched successfully",
      "total": len(ratings),
      "ratings": ratings_json,
      "_links": {
        "self": movie_links['self'],
        "delete": movie_links['delete'],
        "update": movie_links['update'],
        "actors": movie_links['credits'],
        **pagination_links
      }
    }

    return make_response(jsonify(response), 200)
  