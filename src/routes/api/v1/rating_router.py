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
    summary: Fetch all ratings for movies
    description: Retrieves all movie ratings and their details, including the movie     title and rating score. If no ratings are found, a 404 error is returned.
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
                    description: Rating text (e.g., "8/10")
                    example: "8/10"
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
        return controller.get_movie_rating(movie_id)

    return rating_blueprint
