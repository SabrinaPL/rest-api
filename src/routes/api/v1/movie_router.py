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
        """
        Create a new movie
        ---
        tags:
          - Movies
        summary: Create a new movie
        description: Adds a new movie to the database. Requires a     valid JWT access token.
        security:
          - BearerAuth: []
        requestBody:
          required: true
          content:
            application/json:
              schema:
          type: object
          properties:
            title:
              type: string
              description: Title of the movie.
            director:
              type: string
              description: Director of the movie.
            year:
              type: integer
              description: Release year of the movie.
            genre:
              type: string
              description: Genre of the movie.
          required:
            - title
            - director
        responses:
          201:
            description: Movie created successfully
          400:
            description: Bad request (e.g., missing or invalid fields)
          401:
            description: Unauthorized (JWT token missing or invalid)
          500:
            description: Internal server error
        """
        return controller.create_movie()

    # Update a movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['PUT'])
    @jwt_required()
    def update_movie(movie_id):
        """
        Update movie by ID
        ---
        tags:
          - Movies
        summary: Update a movie
        description: Updates an existing movie's details by its unique ID. Requires a valid JWT access token.
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
              description: The unique ID of the movie to update.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  title:
                    type: string
                    description: Updated title of the movie.
                  director:
                    type: string
                    description: Updated director of the movie.
                  year:
                    type: integer
                    description: Updated release year of the movie.
                  genre:
                    type: string
                    description: Updated genre of the movie.
        responses:
          200:
            description: Movie updated successfully
          400:
            description: Bad request (e.g., invalid fields)
          401:
            description: Unauthorized (JWT token missing or invalid)
          404:
            description: Movie not found
          500:
            description: Internal server error
        """
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
