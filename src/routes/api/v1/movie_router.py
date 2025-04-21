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
        summary: Retrieve all movies with optional filters
        description: Fetches all movies from the database with optional filter (e.g. by title, genre, year).
        parameters:
          - name: title
            in: query
            required: false
            schema:
              type: string
            description: Filter movies by title.
          - name: genre 
            in: query
            required: false
            schema:
              type: string
            description: Filter movies by genre.
          - name: release_year
            in: query
            required: false
            schema:
              type: integer
            description: Filter movies by release year.
          - name: description
            in: query
            required: false
            schema:
              type: string
            description: Filter movies by description.
          - name: rating
            in: query
            description: Filter movies by rating.
            required: false
            schema:
              type: number
          - name: actor
            in: query
            description: Filter movies by actor.
            required: false
            schema:
              type: string
          - name: page
            in: query
            required: false
            schema:
              type: integer
              default: 1
            description: Page number for pagination.
          - name: per_page
            in: query
            required: false
            schema:
              type: integer
              default: 20
            description: Number of items per page for pagination.
        responses:
          200:
            description: Movies fetched successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Success message
                  example: Movies fetched successfully
                _links:
                  type: object
                  description: Pagination links
                  example:
                    first: /api/v1/movies?page=1
                    next: /api/v1/movies?page=2
                    last: /api/v1/movies?page=10
                movies:
                  type: array
                  description: List of movies
                  items:
                    type: object
                    properties:
                      description:
                        type: string
                        description: Movie description
                        example: A thrilling adventure of a young hero.
                      title:
                        type: string
                        description: Movie title
                        example: The Great Adventure
                      genre: 
                        type: array
                        description: List of genres
                        example: ["Adventure", "Action"]
                      release_year:
                        type: integer
                        desciption: Release year of the movie
                        example: 2023
                      id:
                        type: string
                        description: Unique ID of the movie
                        example: 12345abcde
                      movie_id:
                        type: string
                        description: Movie ID
                        example: 1234        
          400:
            description: Invalid query parameters
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
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Success message
                  example: Movie fetched successfully
                _links:
                  type: object
                  description: Links to related resources
                  example:
                    self: /api/v1/movies/12345abcde
                    ratings: /api/v1/ratings/12345abcde/ratings
                    actors: /api/v1/credits/actors/12345abcde/actors
                movie:
                  type: object
                  description: Movie description
                  example: Shakespeare's Play transplanted into a 1930s setting.
                genre:
                  type: array
                  description: List of genres
                  example: ["Drama", "Romance"]
                release_year:
                  type: integer
                  description: Release year of the movie
                  example: 1979
                id: 
                  type: string
                  description: Unique ID of the movie
                  example: 12345abcde
                title:
                  type: string
                  description: Movie title
                  example: The Shakespearian Adventure       
          400:
            description: Invalid movie ID format
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
        description: Adds a new movie to the database. Requires a valid JWT access token.
        parameters:
          - name: Authorization
            in: header
            required: true
            schema:
              type: string
              description: Bearer JWT token for authentication.
              example: Bearer <your_jwt_token>
          - name: title
            in: body
            required: true
            schema:
              type: string
              description: Title of the movie.
              example: The Great Adventure
          - name: release_year
            in: body
            required: true
            schema:
              type: integer
              description: Release year of the movie.
              example: 2023
          - name: genres
            in: body
            required: true
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: array
                    description: Genre of the movie.
                    example: Action
                  id:
                    type: integer
                    description: Genre ID.
                    example: 1
          - name: overview
            in: body
            required: false
            schema:
              type: string
              description: Description of the movie.
              example: A thrilling adventure of a young hero.  
        responses:
          201:
            description: Movie created successfully
            schema:
                type: object
                properties:
                  _links:  
                      type: object
                      description: Links to related resources
                      example:
                        self: /api/v1/movies/12345abcde
                        delete: /api/v1/movies/12345abcde
                        update: /api/v1/movies/12345abcde
                  message:
                    type: string
                    description: Success message
                    example: Movie created successfully
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
        parameters:
          - name: Authorization
            in: header
            required: true
            schema:
              type: string
              description: Bearer JWT token for authentication.
              example: Bearer <your_jwt_token>
          - name: movie_id
            in: path
            required: true
            schema:
              type: string
              description: The unique ID of the movie to update.
              example: 12345abcde
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
                    example: The Great Adventure
                  release_year:
                    type: integer
                    description: Release year of the movie.
                    example: 2023
                  genres:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: array
                          description: Genre of the movie.
                          example: Action
                        id:
                          type: integer
                          description: Genre ID.
                          example: 1
                  overview:
                    type: string
                    description: Description of the movie.
                    example: A thrilling adventure of a young hero.   
        responses:
          200:
            description: Movie updated successfully
            schema:     
                type: object
                properties:
                  message:
                    type: string
                    description: Success message
                    example: Movie updated successfully
                  _links:
                    type: object
                    description: Links to related resources
                    example:
                      self: /api/v1/movies/12345abcde
                      delete: /api/v1/movies/12345abcde
                      update: /api/v1/movies/12345abcde
                      actors: /api/v1/credits/actors/12345abcde/actors
                      ratings: /api/v1/ratings/12345abcde/ratings
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
