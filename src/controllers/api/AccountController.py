import bleach
from flask import request, jsonify, make_response
from utils.CustomErrors import CustomError
from utils.validate import validate_fields 

class AccountController:
  def __init__(self, logger, json_web_token, user_model, db_repo, generate_hateoas_links):
    self.json_web_token = json_web_token
    self.user_model = user_model
    self.db_repo = db_repo
    self.logger = logger
    self.generate_hateoas_links = generate_hateoas_links

  # Sanitize req data to improve security and prevent XSS
  def sanitize_data(self, data):
    # Recursively sanitize dictionary keys and values or list items (as suggested by copilot)
    if isinstance(data, dict):
      return {key: self.sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
      return [self.sanitize_data(item) for item in data]
    elif isinstance(data, str):
      # Remove any potentially harmful HTML or JavaScript 
      return bleach.clean(data, strip=True)

  def register(self):
    """
    Register a new user.
    """
    try:
      raw_data = request.get_json()
      sanitized_data = self.sanitize_data(raw_data)
      
      # Validate required fields
      required_fields = ["first_name", "last_name", "username", "password", "email"]
      validate_fields(sanitized_data, required_fields)
      
      # Validate format of field values
      if not self.is_valid_email(sanitized_data.get("email")):
        raise CustomError("Invalid email format", 400)
      
      if not self.is_strong_password(sanitized_data.get("password")):
        raise CustomError("Password must be at least 8 characters long and include a number and a special character", 400)

      # Check if user exists
      existing_user = self.check_user(sanitized_data.get("username"))
      
      if existing_user:
        raise CustomError("Invalid credentials", 400)

      user = self.user_model(
        first_name = sanitized_data.get("first_name"),
        last_name = sanitized_data.get("last_name"),
        username = sanitized_data.get("username"),
        password = sanitized_data.get("password"),
        email = sanitized_data.get("email")
      )

      user.save()
      
      # Convert the user ID to a string for JSON serialization, this is necessary because MongoEngine uses ObjectId which is not JSON serializable
      user_id = str(user.id)

      self.logger.info(f"User registered successfully")
      
      user_links = self.generate_hateoas_links.create_user_links(user_id)
      
      response = {
        "message": "User registered successfully",
        "_links": {
          "self": user_links["self"],
          "delete": user_links["delete"]
        }
      }

      return make_response(jsonify(response), 201)

    except Exception as e:
      self.logger.error(f"Error registering user: {e}")
      raise CustomError("Internal server error", 500)
  
  def login(self):
    """
    Log in a user and return an access token and refresh token.
    """
    self.logger.info("User login attempt")
    
    try:
      raw_data = request.get_json()
      sanitized_data = self.sanitize_data(raw_data)
      
      # Validate required fields
      required_fields = ["username", "password"]
      validate_fields(sanitized_data, required_fields)
  
      # Check if user exists
      existing_user = self.check_user(sanitized_data.get("username"))
      
      if not existing_user:
        raise CustomError("Invalid credentials", 400)

      # Validate password
      if not existing_user.check_password(sanitized_data.get("password")):
        raise CustomError("Invalid credentials", 400)
      
      # Convert user ID for JSON serialization
      user_id = str(existing_user.id)

      # Generate JWT token
      access_token = self.json_web_token.create_access_token(user_id)
      refresh_token = self.json_web_token.create_refresh_token(user_id)

      self.logger.info(f"User logged in successfully")
      
      user_links = self.generate_hateoas_links.create_user_links(user_id)

      response = {
        "message": "User logged in successfully",
        "_links": {
          "self": user_links["self"],
          "delete": user_links["delete"]
        },
        "access_token": access_token,
        "refresh_token": refresh_token
      }

      return make_response(jsonify(response), 200)
    except Exception as e:
      self.logger.error(f"Error logging in user: {e}")
      raise CustomError("Internal server error", 500)

  def refresh(self):
    """
    Refresh the access token using the refresh token.
    """
    self.logger.info("User refresh token attempt")
    
    try:
      # Validate refresh token
      refresh_token = request.headers.get("Authorization")

      if not refresh_token:
        raise CustomError("Refresh token is required", 400)
 
      # Generate a new access token using the identity from the refresh token
      access_token = self.json_web_token.refresh()

      self.logger.info(f"Token refreshed successfully")

      response = {
        "message": "Token refreshed successfully",
        "access_token": access_token
      }

      return make_response(jsonify(response), 200)
    
    except CustomError as e:
      raise e
    except Exception as e:
      self.logger.error(f"Error refreshing token: {e}")
      raise CustomError("Internal server error", 500)

  def check_user(self, username):
      """
      Check if a user with the given username already exists.
      Returns the user object if found, otherwise None.
      """
      return self.db_repo.find_by_field('username', username)
  
  # Helper methods for validation (as suggested by copilot)  
  def is_valid_email(self, email):
    """
    Validate email format.
    """
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

  def is_strong_password(self, password):
    """
    Validate password strength.
    """
    import re
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None
