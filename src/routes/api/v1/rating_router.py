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
        return controller.get_ratings()
    
        # Retrieve a movie rating by ID
    @rating_blueprint.route('/ratings/<movie_id>', methods=['GET'])
    def get_movie_rating(movie_id):
        return controller.get_movie_rating(movie_id)

    return rating_blueprint
