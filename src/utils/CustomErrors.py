from flask import jsonify

# ------------------------------------------------------------------------------------------------ #
# Custom Errors
# ------------------------------------------------------------------------------------------------ #
class CustomError(Exception):
    """_summary_
    Base class for custom errors.
    
    """
    def __init__(self, message, status_code):
      """Inherit from the Exception class and set the error message."""
      self.message = message
      self.status_code = status_code
      super().__init__(self.message)
  
    def to_response(self):
      """Convert error to a JSON response."""
      response = jsonify({"error": self.message})
      response.status_code = self.status_code
      return response

