import flask_jwt_extended

# Utility class for encoding and decoding jwt tokens and jwt refresh tokens using Flask-JWT-Extended
class JsonWebToken:
  def __init__(self, logger):
    self.logger = logger
    pass
  
  def create_access_token(self, data):
    self.logger.info(f"Encoding JWT accecss token")
    return flask_jwt_extended.create_access_token(identity=data)
  
  def create_refresh_token(self, data):
    self.logger.info(f"Encoding JWT refresh token")
    return flask_jwt_extended.create_refresh_token(identity=data)
  
  def decode(self, token):
    self.logger.info(f"Decoding JWT token")
    return flask_jwt_extended.decode_token(token)
  
  def refresh(self):
    self.logger.info(f"Refreshing JWT token")
    identity = flask_jwt_extended.get_jwt_identity()
    return flask_jwt_extended.create_access_token(identity=identity)

# TODO: add error handling!