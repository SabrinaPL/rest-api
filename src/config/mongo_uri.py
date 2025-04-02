import os

def setup_mongo_uri(app):
  """
  Configure the MongoDB URI and set it in the Flask app.
  """
  # Load environment variables from .env file
  mongo_user = os.getenv("MONGO_USER")
  mongo_pass = os.getenv("MONGO_PASS")
  mongo_host = os.getenv("MONGO_HOST")
  mongo_port = os.getenv("MONGO_PORT")
  mongo_db = os.getenv("MONGO_DB")
  flask_env = os.getenv("FLASK_ENV")
  
  if flask_env == "development":
      if mongo_user and mongo_pass:
        mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
      else:
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_db}"
  else:
       mongo_uri = os.getenv("MONGO_URI")

  # Configure env variables into app
  app.config["MONGO_URI"] = mongo_uri
