from flask import Blueprint

health_blueprint = Blueprint('health', __name__)

# Route for health check to verify if the service is running
@health_blueprint.route('/health', methods=['GET'])
def health():
    return "Healthy", 200
