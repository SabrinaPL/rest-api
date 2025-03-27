import flask_jwt_extended

# Class for encoding and decoding jwt tokens and jwt refresh tokens using Flask-JWT-Extended
class JsonWebToken:
  def __init__(self):
    pass
  
  def encode(self, data):
    return flask_jwt_extended.create_access_token(identity=data)
  
  def decode(self, token):
    return flask_jwt_extended.decode_token(token)
  
  def refresh(self, identity):
    return flask_jwt_extended.create_refresh_token(identity=identity)

# TODO add error handling!