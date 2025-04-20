from flask import Blueprint

def create_credit_blueprint(controller):
    """
    Factory function to create the credit blueprint.
    This allows for dependency injection of the logger and controller.
    """
    # Create a Blueprint for credit-related routes
    credit_blueprint = Blueprint('credit', __name__)

    # Get all actors
    @credit_blueprint.route('/credits/actors', methods=['GET'])
    def get_actors():
        """
        Get all actors
        ---
        tags:
          - Credits
        summary: Retrieve all actors with optional filters
        description: Fetches all actors from the database with optional filters.
        parameters:
          - name: actor
            in: query
            required: false
            schema:
              type: string
            description: 
              Filter actors by name.
          - name: page
            in: query
            required: false
            schema:
              type: integer
            description: 
              Page number for pagination.
          - name: per_page
            in: query
            required: false
            schema:
              type: integer
            description: 
              Number of items per page for pagination.
        responses:
          200:
            description: Actors fetched successfully
            schema:
                type: object
                properties:
                  actors:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                          description: The ID of the actor
                          example: "12345"
                        name:
                          type: string
                          description: The name of the actor
                          example: "Matt Dillon"
                        movies_played:
                          type: array
                          items:
                            type: string
                            description: List of movies played by the actor
                            example: ["Movie 1", "Movie 2"]
          400:
            description: Invalid query parameters
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
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Success message
                  example: Actors fetched successfully
                actors:
                  type: array
                  items:
                    type: object
                    properties:
                      cast_id:
                        type: string
                        description: The cast ID of the actor
                      name:
                        type: string
                        description: The name of the actor
                        example: "Matt Dillon"
                      character:
                        type: string
                        description: The character played by the actor
                        example: "Larry Maretto"
                      gender:
                        type: integer
                        description: The actors gender
                        example: 2
                      order:
                        type: integer
                        description: The order of the actor in the cast list
                        example: 1
                      profile_path:
                        type: string
                        description: The path to the actors profile image
                        example: "/path/to/profile.jpg"
                      id:
                        type: string
                        description: The ID of the actor
                        example: "12345"
          400:
            description: Invalid movie ID format
          404:
            description: No movie found or actors found for this movie
          500:
            description: Internal server error
        """
        return controller.get_actors_by_movie(movie_id)

    return credit_blueprint
