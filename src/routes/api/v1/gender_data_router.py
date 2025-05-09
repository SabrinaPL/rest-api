from flask import Blueprint

def create_gender_statistics_blueprint(controller):
    """
    Factory function to create the gender data blueprint.
    This allows for dependency injection of the logger and controller.
    """
    gender_statistics_blueprint = Blueprint('gender_statistics', __name__)
    
    # Get all gender statistics
    @gender_statistics_blueprint.route('/gender-statistics', methods=['GET'])
    def get_gender_data():
      return controller.get_gender_data()
    
    # Get gender statistics by country
    @gender_statistics_blueprint.route('/gender-statistics/country', methods=['GET'])
    def get_gender_statistics_by_country():
      return controller.get_gender_statistics_by_country()
    
    return gender_statistics_blueprint
  