from flask import jsonify, make_response, request
from utils.CustomErrors import CustomError  
from utils.custom_status_codes import CREDIT_CUSTOM_STATUS_CODES
from bson import ObjectId

class ActorController:
  def __init__(self, logger, credit_db_repo, json_convert, generate_hateoas_links, movie_query_service, movie_db_repo):
    self.credit_db_repo = credit_db_repo
    self.movie_db_repo = movie_db_repo
    self.movie_query_service = movie_query_service
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.logger = logger

  def get_actors(self):
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
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[400]["invalid_pagination"], 400)
    
      if query_params:
        self.logger.info("Query parameter provided, fetching actors by filter...")
      
        # Validate the query parameters
        query = self.movie_query_service.build_query('actors', query_params)
        self.logger.info("Query built successfully")
      
        # Replace 'movie_id' with '_id' in the query for the credits collection
        if 'movie_id' in query:
          query['id'] = query.pop('movie_id')
          self.logger.info("Replaced 'movie_id' with 'id' in the query for credits collection")
      else: 
        self.logger.info("Query parameters not provided, fetching all actors...")
        query = {}

      credits = self.credit_db_repo.find_by_query_with_pagination(query, page=page, per_page=per_page)

      if not credits:
        self.logger.info("No credits found")
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[404]["no_credits_found"], 404)

      actor_dict = {}
      actors_json = []

      # Extract actors from credits (as suggested by copilot)
      for credit in credits:
          movie = self.movie_db_repo.find_by_field('movie_id', credit.id)

          if not movie:
              continue
    
          # Filter actors based on query parameters, allow partial matches (as suggested by copilot)          
          for cast_member in credit.cast:
              if query_params.get('actor', '').lower() in cast_member.name.lower():
                if cast_member.id not in actor_dict:
                  actor_dict[cast_member.id] = {
                      "id": cast_member.id,
                      "name": cast_member.name,
                      "movies_played": [],
                  }
                # Add the movie title to the movies_played list if not already present
                if movie.title not in actor_dict[cast_member.id]["movies_played"]:
                  actor_dict[cast_member.id]["movies_played"].append(movie.title)

      actors_json = list(actor_dict.values())

      pagination_links = self.generate_hateoas_links.create_pagination_links("credit.get_actors", page, per_page, len(actors_json))
      self.logger.info("Pagination links generated")

      response = {
        "message": "Actors fetched successfully",
        "total": len(actors_json),
        "actors": actors_json,
        "_links": {
          **pagination_links
        }
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.info(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Unexpected error while fetching actors: {e}")
      raise CustomError(CREDIT_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

  def get_actors_by_movie(self, _id):
    try:
      self.logger.info(f"Fetching actors for movie with ID: {_id}")
    
      # Fetch movie by ID
      try:
        # Convert id to ObjectId
        _id = ObjectId(_id)
      except Exception as e:
        self.logger.error(f"Invalid ID format: {e}")
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[400]["invalid_id"], 400)
    
      movie = self.movie_db_repo.find_by_id(_id)
    
      if not movie:
        self.logger.info(f"Movie with ID {_id} not found")
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[404]["movie_not_found"], 404)
    
      movie_id = str(movie.movie_id)

      credits = self.credit_db_repo.find_by_field("id", movie_id)

      if not credits or len(credits) == 0:
        self.logger.info(f"No actors found for movie with ID {movie_id}")
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[404]["no_credits_found"], 404)

      # Extract all actors from credits
      actors = []
      if hasattr(credits, 'cast'):
        for credit in credits.cast:
          actors.append(credit)

      if not actors:
        self.logger.info(f"No actors found for movie with ID {movie_id}")
        raise CustomError(CREDIT_CUSTOM_STATUS_CODES[404]["no_actors_found"], 404)
    
      # Convert actors to JSON-serializable format
      actors_json = []
      for actor in actors:
          actors_json.append({
              "cast_id": actor.cast_id,
              "character": actor.character,
              "credit_id": actor.credit_id,
              "gender": actor.gender,
              "id": actor.id,
              "name": actor.name,
              "order": actor.order,
              "profile_path": actor.profile_path,
          })
      
      self.logger.info(f"Actors converted to JSON format")

      movie_links = self.generate_hateoas_links.create_movies_links(movie_id, has_actors=True, has_ratings=False)

      response = {
        "message": "Actors fetched successfully",
        "total": len(actors_json),
        "actors": actors_json,
        "_links": {
          "self": movie_links['self'],
          "delete": movie_links['delete'],
          "update": movie_links['update']
        }
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      self.logger.info(f"Custom error occurred: {e}")
      raise e
    except Exception as e:
      self.logger.error(f"Unexpected error while fetching actors: {e}")
      raise CustomError(CREDIT_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
  