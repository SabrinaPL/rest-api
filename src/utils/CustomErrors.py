from flask import jsonify

class CustomError(Exception):
    """_summary_
    Base class for custom errors.
    
    """
    def __init__(self, message, status_code):
      """Inherit from the Exception class and set the error message."""
      super().__init__(message)
      self.message = message
      self.status_code = status_code
  
    def to_response(self):
      """Convert error to a JSON response."""
      return {
        "error": self.message,
        "status_code": self.status_code
        }, self.status_code

