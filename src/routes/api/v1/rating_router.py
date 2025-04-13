from flask import Blueprint

def create_rating_blueprint(controller):
    """
    Factory function to create the rating blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for rating-related routes
    rating_blueprint = Blueprint('rating', __name__)

    # Map HTTP verbs and route paths to controller actions

    # Get all ratings
    @rating_blueprint.route('/ratings', methods=['GET'])
    def get_ratings():
        """
    Fetch all ratings
    ---
    tags:
      - Ratings
    summary: Fetch all ratings for movies with optional filters
    description: Retrieves all movie ratings and their details, including the movie title and rating score, with optional filter (rating and pagination filters). If no ratings are found, a 404 error is returned.
    parameters:
    - name: rating
      in: query
      required: false
      schema:
        type: string
      description: Filter ratings by rating score.
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
        description: Successfully fetched all ratings
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Ratings fetched successfully
            total:
              type: integer
              description: Total number of ratings
              example: 50
            ratings:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique identifier for the rating
                    example: 1
                  text:
                    type: string
                    description: Rating text (e.g., "5/5")
                    example: "5/5"
                  movie:
                    type: string
                    description: The title of the movie being rated
                    example: The Shawshank Redemption
            _links:
              type: object
              properties:
                first:
                  type: string
                  description: Link to the first page of ratings
                  example: /api/v1/ratings?page=1
                next:
                  type: string
                  description: Link to the next page of ratings
                  example: /api/v1/ratings?page=2
                last:
                  type: string
                  description: Link to the last page of ratings
                  example: /api/v1/ratings?page=3
      404:
        description: No ratings found
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message
              example: No ratings found
    """
        return controller.get_ratings()

    # Retrieve a movie rating by ID
    @rating_blueprint.route('/ratings/<movie_id>', methods=['GET'])
    def get_movie_rating(movie_id):
        """
      Fetch movie rating by ID
      ---
      tags:
        - Ratings
      summary: Fetch a movie rating by movie ID
      description: Retrieves the rating details for a specific movie using its unique ID.
      parameters:
      - name: movie_id
        in: path
        required: true
        schema:
          type: string
        description: The unique ID of the movie to retrieve the rating for.
      responses:
        200:
          description: Successfully fetched movie rating
          schema:
            type: object
            properties:
              message:
                type: string
                description: Success message
                example: Rating fetched successfully
              rating:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique identifier for the rating
                    example: 1
                  text:
                    type: string
                    description: Rating text (e.g., "4/5")
                    example: "4/5"
                  movie:
                    type: string
                    description: The title of the rated movie
                    example: The Godfather
        404:
          description: Rating not found
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message
                example: Rating not found
        500:
          description: Internal server error
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message
                example: An unexpected error occurred
        """
        return controller.get_movie_rating(movie_id)

    return rating_blueprint
