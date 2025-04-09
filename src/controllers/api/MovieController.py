from flask import request, jsonify
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
    
    response = {
      "message": "Movies fetched successfully",
      "total": len(movies),
      "movies": movies_json,
      "_links": {
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
      }
    }

    return response, 200
  
  def search_movie(self):
    self.logger.info("Searching for movies with query parameters...")
    
    # Retrieve all query parameters
    query_params = request.args.to_dict()

    if not query_params:
      self.logger.info("No query parameters provided")
      return {"message": "No query parameters provided"}, 400
    
    self.logger.info(f"Query parameters: {query_params}")
    
    # Validate the query parameters
    valid_fields = ['movie_id', 'title', 'year', 'genre', 
                    'actor', 'description', 'rating']
    invalid_fields = [field for field in query_params if field not in valid_fields]
    
    if invalid_fields:
      self.logger.error(f"Invalid query parameters: {', '.join(invalid_fields)}")
      return {"message": f"Invalid query parameters: {', '.join(invalid_fields)}"}, 400
    
    try:
      query = {}
      
      for field, value in query_params.items():
        if field == 'actor':
          # Search the credit db collection for the actor
          self.logger.info(f"Searching for movies with actor: {value}")
          
          query['cast__name__icontains'] = value
    
          credits_for_actor = self.credit_db_repo.find_by_query(query)
          
          # Loop through credits_for_actor and retrieve the _id for all of the objects (movies the actor has acted in)
          movie_ids = [credit.id for credit in credits_for_actor]
          self.logger.info(f"Movie IDs for actor {value}: {movie_ids}")
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'rating':
          self.logger.info(f"Searching for movies with rating: {value}")
          
          query['rating__gte'] = float(value)
          if query['rating__gte'] < 0 or query['rating__gte'] > 5:
            self.logger.error(f"Invalid rating: {query['rating__gte']}")
            return {"message": "Invalid rating"}, 400
          
          movies_by_rating = self.rating_db_repo.find_by_query(query)
          # Loop through ratings and retrieve the _id for all of the objects (movies with the rating)
          movie_ids = [str(rating.movie_id) for rating in movies_by_rating]
          
          self.logger.info(f"Movie IDs for rating {value}: {movie_ids}")
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'genre':
          self.logger.info(f"Searching for movies with genre: {value}")

          query['genres__name__icontains'] = value
          
          movies_of_genre = self.movie_db_repo.find_by_query(query)
          # Loop through genres and retrieve the _id for all of the objects (movies with the genre)
          movie_ids = [movie.movie_id for movie in movies_of_genre]
          self.logger.info(f"Movie IDs for genre {value}: {movie_ids}")
          
          query = {'movie_id': {'$in': movie_ids}}
        elif field == 'description':
          self.logger.info(f"Searching for movies with description: {value}")
          
          query['overview__icontains'] = value        
        elif field == 'year':
          self.logger.info(f"Searching for movies with release year: {value}")

          # Search for movies by year, using datetime to create a date range (as suggested by copilot)
          year = int(value)
          if year < 1900 or year > datetime.now().year:
            self.logger.error(f"Invalid year: {year}")
            return {"message": "Invalid year"}, 400

          start_date = datetime(year, 1, 1)
          end_date = datetime(year, 12, 31, 23, 59, 59)
          query['release_date__gte'] = start_date
          query['release_date__lte'] = end_date
        else:
          # Search for movies by other fields
          self.logger.info(f"Searching for movies with {field}: {value}")

          query[f"{field}__icontains"] = value
      
      # Query the movie database for the movies
      self.logger.info(f"Querying movies with filters: {query}")
      movies = self.movie_db_repo.find_by_query(query)
      
      if not movies:
        self.logger.info("No movies found with the given filters")
        return {"message": "No movies found"}, 404

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
 
      response = {
        "message": "Movies fetched successfully",
        "total": len(movies),
        "movies": movies_json,
        "_links": {
          "first": "/api/v1/movies?page=1",
          "next": f"/api/v1/movies?page=2" if len(movies) > 20 else None,
          "last": f"/api/v1/movies?page={len(movies) // 20}"
        }
      }

      return response, 200    
    
    except Exception as e:
      self.logger.error(f"Error occurred while searching for movies: {e}")
      return {"message": "Internal server error"}, 500

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

    # TODO: Fix hateoas links
    response = {
      "message": "Actors fetched successfully",
      "total": len(actors_json),
      "actors": actors_json,
      "_links": {
        "first": "/api/v1/actors?page=1",
        "next": f"/api/v1/actors?page=2" if len(actors_json) > 10 else None,
        "last": f"/api/v1/actors?page={len(actors_json) // 10}"
      }
    }

    return response, 200
  
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

    response = {
            "message": "Ratings fetched successfully",
            "total": len(ratings),
            "ratings": processed_ratings,
            "_links": {
                "first": "/api/v1/ratings?page=1",
                "next": f"/api/v1/ratings?page=2" if len(ratings) > 10 else None,
                "last": f"/api/v1/ratings?page={len(ratings) // 10}"
            }
        }

    return response, 200

  def get_ratings_by_movie(self, movie_id):
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

    response = {
      "message": "Ratings fetched successfully",
      "total": len(ratings),
      "ratings": ratings_json,
      "_links": {
        "first": f"/api/v1/movies/{movie_id}/ratings?page=1",
        "next": f"/api/v1/movies/{movie_id}/ratings?page=2" if len(ratings) > 10 else None,
        "last": f"/api/v1/movies/{movie_id}/ratings?page={len(ratings) // 10}"
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

    response = {
      "message": "Actors fetched successfully",
      "total": len(actors),
      "actors": actors_json,
      "_links": {
        "first": f"/api/v1/movies/{movie_id}/credits?page=1",
        "next": f"/api/v1/movies/{movie_id}/credits?page=2" if len(actors) > 10 else None,
        "last": f"/api/v1/movies/{movie_id}/credits?page={len(actors) // 10}"
      }
    }
    return response, 200

  def add_movie (self):
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
      # call the DataService to save the movie data
      # TODO: add hateoas links
      self.data_service.save_new_movie(movie_data)
      return jsonify({"message": "Movie added successfully"}), 201
    except Exception as e:
      self.logger.error(f"Error saving movie: {e}")
      return {"message": "Internal server error"}, 500  

  # def update_movie (self, movie_id):

  def delete_movie (self, movie_id):
    self.logger.info(f"Deleting movie with ID: {movie_id}")
    
    # Convert movie id to int since it's stored as an int in the ratings database
    movie_id_int = int(movie_id)
    
    # Delete associated ratings
    self.rating_db_repo.delete_by_field("movie_id", movie_id_int)
    self.logger.info(f"Ratings for movie with ID {movie_id} deleted successfully")

    # Delete the movie
    self.movie_db_repo.delete(movie_id)
    self.logger.info(f"Movie with ID {movie_id} deleted successfully")

    response = {
      "message": "Movie and associated ratings deleted successfully",
    }

    return response, 204

    