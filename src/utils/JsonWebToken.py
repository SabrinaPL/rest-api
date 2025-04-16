import flask_jwt_extended

# Utility class for encoding and decoding jwt tokens and jwt refresh tokens using Flask-JWT-Extended
class JsonWebToken:
  def __init__(self, logger):
    self.logger = logger
    pass
  
  def create_access_token(self, data):
    self.logger.info(f"Creating JWT access token")
    
    try:
      access_token = flask_jwt_extended.create_access_token(identity=data)
      self.logger.info(f"JWT access token created successfully")
    except Exception as error:
      self.logger.info(f"Error creating JWT access token: {error}")
      raise error
      
    return access_token
  
  def create_refresh_token(self, data):
    self.logger.info(f"Creating JWT refresh token")
    
    try:
      refresh_token = flask_jwt_extended.create_refresh_token(identity=data)
      self.logger.info(f"JWT refresh token created successfully")
    except Exception as error:
      self.logger.info(f"Error creating JWT refresh token: {error}")
      raise error
    
    return refresh_token
  
  def decode(self, token):
    self.logger.info(f"Decoding JWT token")
    
    try:
      # Decode the token to extract the identity
      decoded_token = flask_jwt_extended.decode_token(token)
      self.logger.info(f"JWT token decoded successfully")
    except Exception as error:
      self.logger.info(f"Error decoding JWT token: {error}")
      raise error

    return decoded_token

  def refresh(self):
    self.logger.info(f"Refreshing JWT token")
    
    try:
      # Refresh the token to get a new access token
      # Get the user identity from the refresh token
      identity = flask_jwt_extended.get_jwt_identity()
        
      # Generate a new access token
      refreshed_token = flask_jwt_extended.create_access_token(identity=identity)
        
      self.logger.info(f"JWT token refreshed successfully")
    except Exception as error:
      self.logger.info(f"Error refreshing JWT token: {error}")
      raise error

    return refreshed_token
  
  # TODO: add custom error handling for expired tokens and other JWT errors!