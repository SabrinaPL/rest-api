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

    # Get a specific rating by ID
    @rating_blueprint.route('/ratings/<rating_id>', methods=['GET'])
    def get_rating(rating_id):
        return controller.get_rating(rating_id)

    return rating_blueprint
