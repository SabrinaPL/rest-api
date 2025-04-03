import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request
from flasgger import Swagger
from routes.router import main_blueprint
from dotenv import load_dotenv
from config.logger import get_logger
from config.security import configure_talisman
from config.mongo_engine import connect_to_database
from config.jwt import setup_jwt
from config.mongo_uri import setup_mongo_uri
from services.DataService import DataService
from repositories.DBRepo import DBRepo
from controllers.api.AccountController import AccountController
from controllers.api.MovieController import MovieController
from controllers.api.UserController import UserController
from models.UserModel import User
from models.MovieModel import MovieMetaData
from models.CreditsModel import Credit
from models.RatingsModel import Rating
from routes.api.v1.account_router import create_account_blueprint
from routes.api.v1.movie_router import create_movie_blueprint
from routes.api.v1.credit_router import create_credit_blueprint
from routes.api.v1.rating_router import create_rating_blueprint
from routes.api.v1.health import health_blueprint
from utils.JsonWebToken import JsonWebToken
from seed.seed_db import seed_database

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Swagger for API documentation
Swagger(app, template={
    "info": {
        "title": "RESTful Movies API",
        "description": "API documentation for the Movie API",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/api/v1"
})

# TODO: Add rate limiting

# Setup Loguru logger
logger = get_logger()

flask_env = os.getenv("FLASK_ENV")
app.config["FLASK_ENV"] = flask_env

# Set up the mongo URI and configure it to the app
setup_mongo_uri(app)

# Setup JWT authentication
setup_jwt(app)

# Connect MongoEngine to the database
connect_to_database(app)

# Instantiate dependencies to adhere to IoC and DI principles
json_web_token = JsonWebToken(logger)
user_db_repo = DBRepo(User, logger)
movie_db_repo = DBRepo(MovieMetaData, logger)
credit_db_repo = DBRepo(Credit, logger)
rating_db_repo = DBRepo(Rating, logger)
data_service = DataService(logger)
account_controller = AccountController(logger, json_web_token, User, user_db_repo)
movie_controller = MovieController(logger, movie_db_repo, credit_db_repo, rating_db_repo)
user_controller = UserController(logger, user_db_repo)

# Register the main router blueprint
app.register_blueprint(main_blueprint)

# Create and register the remaining blueprints
account_blueprint = create_account_blueprint(account_controller, user_controller)
app.register_blueprint(account_blueprint, url_prefix='/api/v1')
movie_blueprint = create_movie_blueprint(movie_controller)
app.register_blueprint(movie_blueprint, url_prefix='/api/v1')
credit_blueprint = create_credit_blueprint(movie_controller)
app.register_blueprint(credit_blueprint, url_prefix='/api/v1')
rating_blueprint = create_rating_blueprint(movie_controller)
app.register_blueprint(rating_blueprint, url_prefix='/api/v1')

# Health check route
app.register_blueprint(health_blueprint)

# Seed the database with extracted movie data, if neccessary
seed_database(data_service, logger)

# Log each request
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

# Log unhandled errors
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {e}")
    return {"error": "Internal Server Error"}, 500

if flask_env == "production":
    # Configure Flask-Talisman for security headers in production
    configure_talisman(app, logger)
else:
    logger.info("⚠️ Running in development mode, security headers are not applied.")

if __name__ == "__main__":
    logger.info("🚀 Starting Flask API...")
    port = int(os.getenv("PORT", 5000))
    print(port)
    app.run(host="0.0.0.0", port=port)
