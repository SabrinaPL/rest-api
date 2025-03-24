import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from config.logger import get_logger
from config.security import configure_talisman
from config.mongo_engine import connect_to_database

# Load environment variables
load_dotenv()

# TODO: Add rate limiting

# Setup Loguru logger
logger = get_logger()

# Initialize Flask app
app = Flask(__name__)

# Configure env variables into app
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Setup JWT authentication
jwt = JWTManager(app)

# Apply Flask-Talisman security settings
talisman = configure_talisman(app)

# Connect MongoEngine to the database
connect_to_database(app)

# TODO: Register Blueprints?

# Log each request
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

# Log unhandled errors
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {e}")
    return {"error": "Internal Server Error"}, 500

@app.route("/")
def home():
    return {
        "message": "Welcome to the Movie API!",
        "endpoints": {
            "movies": "/api/v1/movies",
            "actors": "/api/v1/actors",
            "ratings": "/api/v1/ratings"
        }
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Flask API...")
    app.run(host="0.0.0.0", port=3000, debug=True)
