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
        return controller.get_movies()

    # Get a specific movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['GET'])
    def get_movie(movie_id):
        return controller.get_movie(movie_id)
      
    # Add a new movie
    @movie_blueprint.route('/movies', methods=['POST'])
    @jwt_required()
    def add_movie():
        return controller.add_movie()
      
    # Update a movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['PUT'])
    @jwt_required()
    def update_movie(movie_id):
        return controller.update_movie(movie_id)
      
    # Delete a movie by ID
    @movie_blueprint.route('/movies/<movie_id>', methods=['DELETE'])
    @jwt_required()
    def delete_movie(movie_id):
        return controller.delete_movie(movie_id)
      
    # Retrieve a movie rating by ID
    @movie_blueprint.route('/movies/<movie_id>/rating', methods=['GET'])
    def get_movie_rating(movie_id):
        return controller.get_movie_rating(movie_id)

    return movie_blueprint
