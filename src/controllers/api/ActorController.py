from flask import jsonify, make_response
from utils.CustomErrors import CustomError  

class ActorController:
  def __init__(self, credit_db_repo, json_convert, generate_hateoas_links, logger):
    self.credit_db_repo = credit_db_repo
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.logger = logger

  def get_actors(self):
    self.logger.info("Fetching all actors")

    credits = self.credit_db_repo.find_all()

    if not credits:
      self.logger.info("No credits found")
      raise CustomError("Not found", 404)

    actor_dict = {}
    actors_json = []

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
    }

    return make_response(jsonify(response), 200)

  def get_actors_by_movie(self, movie_id):
    self.logger.info(f"Fetching actors for movie with ID: {movie_id}")

    credits = self.credit_db_repo.find_by_id(movie_id)

    if not credits:
      self.logger.info(f"No actors found for movie with ID {movie_id}")
      raise CustomError("Not found", 404)

    # Extract all actors from credits
    actors = []
    if hasattr(credits, 'cast'):
      for credit in credits.cast:
        actors.append(credit)

    if not actors:
      self.logger.info(f"No actors found for movie with ID {movie_id}")
      raise CustomError("Not found", 404)

    # Convert actors to JSON format
    actors_json = self.json_convert.serialize_documents(actors)
    self.logger.info("Actors converted to JSON format")
    
    movie_links = self.generate_hateoas_links.create_movies_links(movie_id)
    pagination_links = self.generate_hateoas_links.create_pagination_links("credit.get_actors_by_movie", 1, 20, len(actors_json), movie_id=movie_id)
    self.logger.info("Pagination links generated")

    response = {
      "message": "Actors fetched successfully",
      "total": len(actors),
      "actors": actors_json,
      "_links": {
        "self": movie_links['self'],
        "delete": movie_links['delete'],
        "update": movie_links['update'],
        "ratings": movie_links['ratings'],
        **pagination_links
      }
    }

    return make_response(jsonify(response), 200)
  