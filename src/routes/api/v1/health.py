from flask import Blueprint

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health', methods=['GET'])

def health():
    """
    Health Check Endpoint
    ---
    tags:
      - Health
    summary: Health check for the API
    description: Returns a simple message to indicate that the API is running.
    responses:
      200:
        description: Service is healthy
        content:
          text/plain:
            schema:
              type: string
              example: Healthy
    """
    return "Healthy", 200
