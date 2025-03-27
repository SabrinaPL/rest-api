import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request
from flask_jwt_extended import JWTManager
from routes.router import main_blueprint
from dotenv import load_dotenv
from config.logger import get_logger
from config.security import configure_talisman
from config.mongo_engine import connect_to_database
from services.DataService import DataService
from seed.seed_db import seed_database

# Load environment variables
load_dotenv()

# Construct the MongoDB URI
mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("MONGO_DB")

if mongo_user and mongo_pass:
    mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
else:
    mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"

# TODO: Add rate limiting

# Setup Loguru logger
logger = get_logger()

# Initialize Flask app
app = Flask(__name__)

# Configure env variables into app
app.config["MONGO_URI"] = mongo_uri
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Register the main router Blueprint
app.register_blueprint(main_blueprint)

# Setup JWT authentication
jwt = JWTManager(app)

# Apply Flask-Talisman security settings
talisman = configure_talisman(app)

# Connect MongoEngine to the database
connect_to_database(app)

# Instantiate dependencies to adhere to IoC and DI principles
data_service = DataService()

# Seed the database with extracted movie data
seed_database(data_service)

# Log each request
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

# Log unhandled errors
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled error: {e}")
    return {"error": "Internal Server Error"}, 500

if __name__ == "__main__":
    logger.info("🚀 Starting Flask API...")
    app.run(host="0.0.0.0", port=3000, debug=True)
