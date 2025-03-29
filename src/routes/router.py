from flask import Blueprint, jsonify
from .api.v1.router import v1_blueprint

# Create the main router Blueprint
main_blueprint = Blueprint('main', __name__)

# Use '/api/v1' as the base path for version 1 of the API
main_blueprint.register_blueprint(v1_blueprint, url_prefix='/api/v1')

# TODO: Move IoC and DI to the main router

# Catch 404 errors
@main_blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404