
class RatingController:
  def __init__(self, rating_db_repo, movie_db_repo, json_convert, generate_hateoas_links, logger):
    self.rating_db_repo = rating_db_repo
    self.movie_db_repo = movie_db_repo
    self.json_convert = json_convert
    self.generate_hateoas_links = generate_hateoas_links
    self.logger = logger
 
  def get_ratings(self):
    self.logger.info("Fetching all ratings")

    ratings = self.rating_db_repo.find_all()

    if not ratings:
      self.logger.info("No ratings found")
      return {"message": "No ratings found"}, 404

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
        
        pagination_links = self.generate_hateoas_links.create_pagination_links("rating.get_ratings", 1, 20, len(ratings_json))
        self.logger.info("Pagination links generated")

    response = {
            "message": "Ratings fetched successfully",
            "total": len(ratings),
            "ratings": processed_ratings,
            "_links": {
                **pagination_links
            }
        }, 200

    return response

  def get_movie_rating(self, movie_id):
    self.logger.info(f"Fetching ratings for movie with ID: {movie_id}")

    # Convert movie id to int since it's stored as an int in the ratings database collection
    movie_id_int = int(movie_id)

    ratings = self.rating_db_repo.find_by_field("movie_id", movie_id_int)

    if not ratings:
      self.logger.info(f"No ratings found for movie with ID {movie_id}")
      return {"message": "No ratings found for this movie"}, 404

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
    }, 200

    return response
  