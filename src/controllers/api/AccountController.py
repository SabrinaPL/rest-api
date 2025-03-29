import bleach
from flask import request, jsonify
from utils.JsonWebToken import JsonWebToken
from models.UserModel import User

class AccountController:
  def __init__(self, logger):
    self.logger = logger
    
  # Sanitize req data to improve security and prevent XSS
  def sanitize_data(self, data):
    return

  # Funcs to register and login users
  def register_user(self, user_data):
    try:
      raw_data = request.get_json()
      
      sanitized_data = self.sanitize_data(raw_data)
      
      user = User(
        first_name = sanitized_data.get("first_name"),
        last_name = sanitized_data.get("last_name"),
        username = sanitized_data.get("username"),
        password = sanitized_data.get("password"),
        email = sanitized_data.get("email")
      )
      
      # TODO: Make sure that the user doesn't already exist
      
       
    except Exception e:
      self.logger.error(f"Error registering user: {e}")
      return jsonify({"error": "Internal server error"}), 500
  
  # def login_user(self, user_data):
  
  # def login_user_refresh(self, user_data):