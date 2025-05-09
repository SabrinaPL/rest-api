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
    
    # Get gender statistics by production country
    @gender_statistics_blueprint.route('/gender-statistics/country', methods=['GET'])
    def get_gender_statistics_by_country():
      return controller.get_gender_statistics_by_country()
    
    # Get gender statistics by production company
    @gender_statistics_blueprint.route('/gender-statistics/company', methods=['GET'])
    def get_gender_statistics_by_company():
      return controller.get_gender_statistics_by_company()
    
    # Get gender statistics by movie genre
    @gender_statistics_blueprint.route('/gender-statistics/genre', methods=['GET'])
    def get_gender_statistics_by_genre():
      return controller.get_gender_statistics_by_genre()
    
    # Get gender statistics by department
    @gender_statistics_blueprint.route('/gender-statistics/department', methods=['GET'])
    def get_gender_statistics_by_department():
      return controller.get_gender_statistics_by_department()

    # Get gender statistics by year
    @gender_statistics_blueprint.route('/gender-statistics/year', methods=['GET'])
    def get_gender_statistics_by_year():
      return controller.get_gender_statistics_by_year()
    
    return gender_statistics_blueprint
  