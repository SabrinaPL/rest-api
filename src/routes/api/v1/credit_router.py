from flask import Blueprint

def create_credit_blueprint(controller):
    """
    Factory function to create the credit blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for credit-related routes
    credit_blueprint = Blueprint('credit', __name__)

    # Map HTTP verbs and route paths to controller actions

    # Get all actors
    @credit_blueprint.route('/credits/actors', methods=['GET'])
    def get_actors():
        """
        Get all actors
        ---
        tags:
          - Credits
        summary: Retrieve all actors
        description: Fetches all actors from the database.
        responses:
          200:
            description: Actors fetched successfully
          404:
            description: No actors found
          500:
            description: Internal server error
        """
        return controller.get_actors()

    # Get actors by movie ID
    @credit_blueprint.route('/credits/actors/<movie_id>', methods=['GET'])
    def get_actors_by_movie(movie_id):
        """
        Get actors by movie ID
        ---
        tags:
          - Credits
        summary: Retrieve actors by movie ID
        description: Fetches all actors associated with a specific movie using its unique ID.
        parameters:
          - name: movie_id
            in: path
            required: true
            schema:
              type: string
              description: The unique ID of the movie.
        responses:
          200:
            description: Actors fetched successfully
          404:
            description: No actors found for this movie
          500:
            description: Internal server error
        """
        return controller.get_actors_by_movie(movie_id)

    return credit_blueprint
