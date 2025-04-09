from flask import Blueprint
from flask_jwt_extended import jwt_required

def create_movie_blueprint(controller):
    """
    Factory function to create the movie blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for movie-related routes
    movie_blueprint = Blueprint('movie', __name__)

    # Map HTTP verbs and route paths to controller actions

    # Get all movies
    @movie_blueprint.route('/movies', methods=['GET'])
    def get_movies():
        """
        Get all movies
        ---
        tags:
          - Movies
        summary: Retrieve all movies
        description: Fetches all movies from the database.
        responses:
          200:
            description: Movies fetched successfully
          404:
            description: No movies found
          500:
            description: Internal server error
        """
        return controller.get_movies()
      
    # Search for a specific movie
    @movie_blueprint.route('/movies/search', methods=['GET'])
    def search_movie():
        """
        Search for a specific movie
        ---
        tags:
          - Movies
        summary: Search for a movie
        description: Searches for a movie based on a specific field and value.
        parameters:
          - name: field
            in: query
            required: true
            schema:
              type: string
              description: The field to search by (e.g., title, genre).
          - name: value
            in: query
            required: true
            schema:
              type: string
              description: The value to search for.
        responses:
          200:
            description: Movie found successfully
          404:
            description: Movie not found
          500:
            description: Internal server error
        """
        return controller.search_movie()

    # Get a specific movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['GET'])
    def get_movie_by_id(movie_id):
        """
        Get movie by ID
        ---
        tags:
          - Movies
        summary: Retrieve movie by ID
        description: Fetches a specific movie using its unique ID.
        parameters:
          - name: movie_id
            in: path
            required: true
            schema:
              type: string
              description: The unique ID of the movie.
        responses:
          200:
            description: Movie fetched successfully
          404:
            description: Movie not found
          500:
            description: Internal server error
        """
        return controller.get_movie_by_id(movie_id)
      
    # Add a new movie
    @movie_blueprint.route('/movies', methods=['POST'])
    @jwt_required()
    def create_movie():
        return controller.create_movie()

    # Update a movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['PUT'])
    @jwt_required()
    def update_movie(movie_id):
        return controller.update_movie(movie_id)
      
    # Delete a movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['DELETE'])
    @jwt_required()
    def delete_movie(movie_id):
        """
        Delete movie by ID
        ---
        tags:
          - Movies
        summary: Delete a movie
        description: Deletes a movie from the database using its unique ID. Requires a valid JWT access token.
        security:
          - BearerAuth: []
        parameters:
          - name: Authorization
            in: header
            required: true
            schema:
              type: string
              description: Bearer JWT token for authentication.
          - name: movie_id
            in: path
            required: true
            schema:
              type: string
              description: The unique ID of the movie to delete.
        responses:
          200:
            description: Movie deleted successfully
          404:
            description: Movie not found
          500:
            description: Internal server error
        """
        return controller.delete_movie(movie_id)

    return movie_blueprint
