import flask_jwt_extended

# Utility class for encoding and decoding jwt tokens and jwt refresh tokens using Flask-JWT-Extended
class JsonWebToken:
  def __init__(self, logger):
    self.logger = logger
    pass
  
  def encode(self, data):
    self.logger.info(f"Encoding JWT token")
    return flask_jwt_extended.create_access_token(identity=data)
  
  def decode(self, token):
    self.logger.info(f"Decoding JWT token")
    return flask_jwt_extended.decode_token(token)
  
  def refresh(self, identity):
    self.logger.info(f"Refreshing JWT token")
    return flask_jwt_extended.create_refresh_token(identity=identity)

# TODO: add error handling!