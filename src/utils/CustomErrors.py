from flask import jsonify

class CustomError(Exception):
    """_summary_
    Base class for custom errors.
    
    """
    def __init__(self, message, status_code, error_code=None):
      """Inherit from the Exception class and set the error message."""
      self.message = message
      self.status_code = status_code
      self.error_code = error_code
      super().__init__(self.message)
  
    def to_response(self):
      """Convert error to a JSON response."""
      response = {
        "error": self.message,
        "error_code": self.error_code if self.error_code else "UNKNOWN_ERROR",
        }
      return jsonify(response), self.status_code

