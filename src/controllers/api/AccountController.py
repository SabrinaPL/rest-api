import bleach
import mongoengine as m_engine
from flask import request, jsonify
from models.UserModel import User

class AccountController:
  def __init__(self, logger, json_web_token):
    self.json_web_token = json_web_token
    self.logger = logger

  # Sanitize req data to improve security and prevent XSS
  def sanitize_data(self, data):
    # Recursively sanitize dictionary keys and values or list items
    if isinstance(data, dict):
      return {key: self.sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
      return [self.sanitize_data(item) for item in data]
    elif isinstance(data, str):
      # Remove any potentially harmful HTML or JavaScript 
      return bleach.clean(data, strip=True)

  def register(self):
    try:
      raw_data = request.get_json()
      
      sanitized_data = self.sanitize_data(raw_data)
      
      # Check if user exists
      existing_user = self.check_user(sanitized_data.get("username"), sanitized_data.get("email"))
      
      if existing_user:
        return jsonify({"error": "Invalid credentials"}), 400

      user = User(
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
      
      response = {
        "message": "User registered successfully",
        "_links": {
          "self": f"/api/v1/users/{user_id}",
          "update": f"/api/v1/users/{user_id}",
          "delete": f"/api/v1/users/{user_id}",
          "login": "/api/v1/users/login",
          "refresh": "/api/v1/users/login/refresh"
        }
      }
      return jsonify(response), 201

    except Exception as e:
      self.logger.error(f"Error registering user: {e}")
      return jsonify({"error": "Internal server error"}), 500
  
  def login(self):
    self.logger.info("User login attempt")
    
    try:
      raw_data = request.get_json()
      
      sanitized_data = self.sanitize_data(raw_data)
  
      # Check if user exists
      existing_user = self.check_user(sanitized_data.get("username"), sanitized_data.get("email"))
      
      if not existing_user:
        return jsonify({"error": "Invalid credentials"}), 400

      # Validate password
      if not existing_user.check_password(sanitized_data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 400

      # Generate JWT token
      token = self.json_web_token.encode(existing_user.id)

      self.logger.info(f"User logged in successfully")

      response = {
        "message": "User logged in successfully",
        "_links": {
          "self": f"/api/v1/users/{existing_user.id}",
          "update": f"/api/v1/users/{existing_user.id}",
          "delete": f"/api/v1/users/{existing_user.id}",
          "login": "/api/v1/users/login",
          "refresh": "/api/v1/users/login/refresh"
        },
        "token": token
      }
      return jsonify(response), 200
    except Exception as e:
      self.logger.error(f"Error logging in user: {e}")
      return jsonify({"error": "Internal server error"}), 500
    
  
  # def login_refresh(self):

  def check_user(self, username, email):
      """
      Check if a user with the given username or email already exists.
      Returns the user object if found, otherwise None.
      """
      try:
        return User.objects(
          m_engine.Q(username=username) | 
          m_engine.Q(email=email)
        ).first()
      except Exception as e:
        self.logger.error(f"Error checking if user exists: {e}")
        return None