from flask import url_for
from flask import current_app

# TODO: Add links to related resources - url for method (generates url for a specific resource, links can be generated)

# DI the app context
class GenerateHateoasLinks:
  def __init__(self, logger, app):
    self.logger = logger
    self.app = app
    
  def create_movies_links(self, movie_id):  
    with self.app.app_context():
      get_movie_url = url_for("movie.get_movie_by_id", movie_id=movie_id, _external=True)
      # update_movie_url = url_for("movie.update_movie", movie_id=movie_id, _external=True)
      delete_movie_url = url_for("movie.delete_movie", movie_id=movie_id, _external=True)
      get_movie_actors = url_for("credit.get_actors_by_movie", movie_id=movie_id, _external=True)
      # get_movie_ratings = url_for("rating.get_ratings_by_movie", movie_id=movie_id, _external=True)

      links = {
        "self": get_movie_url,
        "delete": delete_movie_url,
        "credits": get_movie_actors,
      }
      
      return links

  def create_user_links(self, user_id):
    with self.app.app_context():
      delete_user_url = url_for("user.delete_user", user_id=user_id, _external=True)
      login_user_url = url_for("user.login", user_id=user_id, _external=True)

      links = {
        "login": login_user_url,
        "delete": delete_user_url
      }

      return links


# Create movie
# - Delete the movie{movie_id}
# - Update the movie{movie_id}

# Delete movie

# Update movie
# - Delete movie

# Get all movies

# Get movie info{movie_id}
# - Get a movies actors
# - Ger reviews connected to that movie
# - Delete movie
# - Update movie

# Get a movies actors
# - Get a movies ratings

# Retrieve all movies

# Retrieve all reviews

# User register
# - User login{user_id}
# - Delete user{user_id}

# User login
# - Delete user{user_id}


# _played)
# - **Rating** (id, text, movie)

# - The API **SHOULD** proper HTTP methods.
# - The API **MUST** implement HATEOAS (Hypermedia as the Engine of Application State).
# - The API **MUST** include the following endpoints:
#   - `GET /movies` - Retrieve all movies.
#   - `GET /movies/{id}` - Get details of a specific movie.
#   - `POST /movies` - Add a new movie (**Requires authentication**).
#   - `PUT /movies/{id}` - Update a movie (**Requires authentication**).
#   - `DELETE /movies/{id}` - Delete a movie (**Requires authentication**).
#   - `GET /movies/{id}/ratings` - Retrieve ratings for a specific movie.
#   - `GET /actors` - Retrieve all actors.
#   - `GET /ratings` - Retrieve all ratings.
# - The API **MUST** support query parameters for filtering (e.g., `GET /movies?genre=Action&year=2020`).

