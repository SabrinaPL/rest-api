from flask import url_for
from flask import current_app

# TODO: Add links to related resources - url for method (generates url for a specific resource, links can be generated)

# DI the app context
class GenerateHateoasLinks:
  def __init__(self, logger, app):
    self.logger = logger
    self.app = app
    
  def create_movies_links(self, movie_id):
    
    # Test constructing get_movie_by_id
    
    with self.app.app_context():
      url = url_for("movie.get_movie_by_id", movie_id=movie_id, _external=True)
      
      print('printing url:')
      print(url)

      links = {
        "self": url_for("movie.get_movie_by_id", movie_id=movie_id, _external=True),
      }

  # def create_user_links(self, user_id):


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

