from flask import url_for

class GenerateHateoasLinks:
  def __init__(self, logger, app):
    self.logger = logger
    self.app = app
    
  def create_movies_links(self, movie_id, has_actors, has_ratings):
    with self.app.app_context():
        # Generate basic movie links
        get_movie_url = url_for("movie.get_movie_by_id", movie_id=movie_id, _external=True)
        update_movie_url = url_for("movie.update_movie", movie_id=movie_id, _external=True)
        delete_movie_url = url_for("movie.delete_movie", movie_id=movie_id, _external=True)

        # Initialize the links dictionary with basic links
        links = {
            "self": get_movie_url,
            "update": update_movie_url,
            "delete": delete_movie_url,
        }
        
        # Conditionally add the actors link if has_actors is True
        if has_actors:
            links["actors"] = url_for("credit.get_actors_by_movie", movie_id=movie_id, _external=True)
            
        # Conditionally add the ratings link if has_ratings is True
        if has_ratings:
            links["ratings"] = url_for("rating.get_movie_rating", movie_id=movie_id, _external=True)

        return links

  def create_user_links(self, user_id):
    with self.app.app_context():
      delete_user_url = url_for("account.delete", user_id=user_id, _external=True)

      links = {
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
      page = int(page)
      per_page = int(per_page)
      total_pages = (total + per_page - 1) // per_page  # Calculate total pages

      next_page = page + 1 if page < total_pages else None
      previous_page = page - 1 if page > 1 else None

      # Per page is added to the URL to allow the client to specify the number of items per page
      pagination_links = {
          "first": f"{base_url}?page={page}&per_page={per_page}",
          "next": f"{base_url}?page={next_page}&per_page={per_page}" if next_page else None,
          "previous": f"{base_url}?page={previous_page}&per_page={per_page}" if previous_page else None,
          "last": f"{base_url}?page={total_pages}&per_page={per_page}" if total_pages > 0 else None,
      }

      return pagination_links
