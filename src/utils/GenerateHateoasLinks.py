from flask import url_for

class GenerateHateoasLinks:
  def __init__(self, logger, app):
    self.logger = logger
    self.app = app
    
  def create_movies_links(self, movie_id):  
    with self.app.app_context():
      get_movie_url = url_for("movie.get_movie_by_id", movie_id=movie_id, _external=True)
      update_movie_url = url_for("movie.update_movie", movie_id=movie_id, _external=True)
      delete_movie_url = url_for("movie.delete_movie", movie_id=movie_id, _external=True)
      get_movie_actors = url_for("credit.get_actors_by_movie", movie_id=movie_id, _external=True)
      get_movie_ratings = url_for("rating.get_movie_rating", movie_id=movie_id, _external=True),

      links = {
        "self": get_movie_url,
        "update": update_movie_url,
        "delete": delete_movie_url,
        "actors": get_movie_actors,
        "ratings": get_movie_ratings
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
    
  def create_pagination_links(self, resource, page, per_page, total, **kwargs):
    """
    Generates pagination links for a resource.
    """
    with self.app.app_context():
      base_url = url_for(resource, _external=True, **kwargs)
         
      # Validate inputs (as suggested by copilot)
      page = int(page) if page else 1
      per_page = int(per_page) if per_page else 20
      total_pages = (total + per_page - 1) // per_page  # Calculate total pages

      next_page = page + 1 if page < total_pages else None

      # Per page is added to the URL to allow the client to specify the number of items per page
      pagination_links = {
          "first": f"{base_url}?page={page}&per_page={per_page}",
          "next": f"{base_url}?page={next_page}&per_page={per_page}" if next_page else None,
          "last": f"{base_url}?page={total_pages}&per_page={per_page}" if total_pages > 0 else None,
      }

      return pagination_links
  
  def generate_image_url(self, base_url, image_path):
    """
    Generates a full URL for an image using the base URL and image path.
    """
    if not image_path:
      return None
        
    # Check if the image path is already a full URL
    if image_path.startswith("http://") or image_path.startswith("https://"):
      return image_path
          
    # If not, construct the full URL using the base URL and image path
    return f"{https://image.tmdb.org/t/p/}{image_path}"


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

