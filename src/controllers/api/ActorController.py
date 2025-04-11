  
class ActorController:
  def __init__(self, credit_db_repo, json_convert, generate_hateoas_links, logger):
    self.credit_db_repo = credit_db_repo
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.logger = logger

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
    }, 200

    return response
  