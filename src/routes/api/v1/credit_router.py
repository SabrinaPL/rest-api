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
        return controller.get_actors()

    # Get actors by movie ID
    @credit_blueprint.route('/credits/<movie_id>/actors', methods=['GET'])
    def get_actors_by_movie(movie_id):
        return controller.get_actors_by_movie(movie_id)

    return credit_blueprint
