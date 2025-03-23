from flask import jsonify

# ------------------------------------------------------------------------------------------------ #
# Custom Errors
# ------------------------------------------------------------------------------------------------ #
class CustomError(Exception):
    """_summary_
    Base class for custom errors.
    
    """
    def __init__(self, message):
      """Inherit from the Exception class and set the error message."""
      self.message = message
      super().__init__(self.message)
  
    def to_response(self):
      """Convert error to a JSON response."""
      response = jsonify({"error": self.message})
      response.status_code = self.status_code
      return response
    
    REGISTER_CUSTOM_STATUS_CODES = {
    400: "The request cannot be processed due to a client error (e.g., validation error).",
    409: "The username and/or email address is already registered.",
    500: "An undefined error occurred."
    }

    LOGIN_CUSTOM_STATUS_CODES = {
    401: "Credentials invalid or not provided.",
    500: "An unexpected condition was encountered."
    }
