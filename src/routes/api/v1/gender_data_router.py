from flask import Blueprint

def create_gender_statistics_blueprint(controller):
    """
    Factory function to create the gender data blueprint.
    This allows for dependency injection of the logger and controller.
    """
    gender_statistics_blueprint = Blueprint('gender_statistics', __name__)
    
    # Get all gender statistics data sorted by person (cast or crew)
    @gender_statistics_blueprint.route('/gender-statistics', methods=['GET'])
    def get_gender_data():
      """
      Get gender statistics data sorted by person (cast or crew).
      ---
      tags:
        - Gender Statistics
      summary: Retrieve all gender statistics data, sorted by person (cast or crew), with optional custom pagination.
      description: Fetches all gender statistics data from the database with optional custom pagination.
      parameters:
        - name: page
          in: query
          description: Page number for pagination (default is 1).
          required: false
          schema:
            type: integer
        - name: per_page
          in: query
          description: Number of records per page (default is 100, max is 100).
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender statistics data fetched successfully.
      """
      return controller.get_gender_data()
    
    # Get gender statistics by production country
    @gender_statistics_blueprint.route('/gender-statistics/country', methods=['GET'])
    def get_gender_statistics_by_country():
      """
      Get aggregated and computed gender statistics by production country.
      If no country is provided, it fetches data for all countries.
      ---
      tags:
        - Gender Statistics
      summary: Retrieve gender distribution statistics (in numbers and percentages) based on production country.
      description: Fetches gender distribution statistics for all production countries unless a specific production country is provided.
      parameters:
        - name: country
          in: query
          description: Country code for production country, e.g. US.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender distribution statistics by production country fetched successfully.
      """
      return controller.get_gender_statistics_by_country()
    
    # Get gender statistics by production company
    @gender_statistics_blueprint.route('/gender-statistics/company', methods=['GET'])
    def get_gender_statistics_by_company():
      """
      Get aggregated and computed gender statistics by production company.
      If no company is provided, it fetches data for all companies.
      ---
      tags:
        - Gender Statistics
      summary: Retrieve gender distribution statistics (in numbers and percentages) based on production company.
      description: Fetches gender distribution statistics for all production companies unless a specific production company is provided.
      parameters:
        - name: company
          in: query
          description: Name of the production company.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender distribution statistics by production company fetched successfully.
      """
      return controller.get_gender_statistics_by_company()
    
    # Get gender statistics by movie genre
    @gender_statistics_blueprint.route('/gender-statistics/genre', methods=['GET'])
    def get_gender_statistics_by_genre():
      """
      Get aggregated and computed gender statistics by movie genre.
      If no genre is provided, it fetches data for all genres.
      ---
      tags:
        - Gender Statistics
      summary: Retrieve gender distribution statistics (in numbers and percentages) based on movie genre.
      description: Fetches gender distribution statistics for all genres unless a specific genre is provided.
      parameters:
        - name: genre
          in: query
          description: Movie genre, e.g. Action, Comedy.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender distribution statistics by movie genre fetched successfully.
      """
      return controller.get_gender_statistics_by_genre()
    
    # Get gender statistics by department
    @gender_statistics_blueprint.route('/gender-statistics/department', methods=['GET'])
    def get_gender_statistics_by_department():
      """
      Get aggregated and computed gender statistics by department
      If no department is provided, it fetches data for all departments.
      ---
      tags:
        - Gender Statistics
      summary: Retrieve gender distribution statistics (in numbers and percentages) based on department, e.g. Directing.
      description: Fetches gender distribution statistics for all departments unless a specific department is provided.
      parameters:
        - name: department
          in: query
          description: Department name, e.g. Directing, Acting.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender distribution statistics by department fetched successfully.
      """
      return controller.get_gender_statistics_by_department()

    # Get gender statistics by year
    @gender_statistics_blueprint.route('/gender-statistics/year', methods=['GET'])
    def get_gender_statistics_by_year():
      """
      Get aggregated and computed gender statistics by production year.
      If no production year is provided, it fetches data for all available years.
      ---
      tags:
        - Gender Statistics
      summary: Retrieve gender distribution statistics (in numbers and percentages) based on production year.
      description: Fetches gender distribution statistics for all available production years unless a specific year is provided.
      parameters:
        - name: year
          in: query
          description: Production year, e.g. 1995.
          required: false
          schema:
            type: integer
      responses:
        200:
          description: Gender distribution statistics by production country fetched successfully.
      """
      return controller.get_gender_statistics_by_year()
    
    return gender_statistics_blueprint
  