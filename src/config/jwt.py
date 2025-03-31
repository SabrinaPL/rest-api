import os
from datetime import timedelta
from flask_jwt_extended import JWTManager

def setup_jwt(app):
  # Load config settings from .env
  app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
  
  access_token_expires = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # Default to 1 hour if not set
  refresh_token_expires = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 86400))  # Default to 24 hours if not set
  
  # Convert expiration times to timedelta
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=access_token_expires)
  app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=refresh_token_expires)

  app.config["JWT_COOKIE_SECURE"] = os.getenv("JWT_COOKIE_SECURE")
  app.config["JWT_COOKIE_LOCATION"] = os.getenv("JWT_COOKIE_LOCATION")

  jwt = JWTManager(app)
  
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return {
      "error": "Token has expired",
      "status": 401
    }, 401
