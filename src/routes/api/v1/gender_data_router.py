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
          schema:
            type: object
            properties:
              country:
                type: string
                description: The country code for the production country.
                example: US
              count:
                type: integer
                description: The number of people (cast or crew) involved in movie production from that production country.
                example: 275
              percentage:
                type: number
                format: float
                description: The percentage of male, female and undefined that have worked in movie productions produced in that country.
                example: 30.37777
              gender:
                type: number
                description: The gender of the person (cast or crew) in the movie production. 1 = female, 2 = male, 0 = undefined.
                example: 2 
        500:
          description: An unexpected error occurred while processing the request.
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message.
                example: "An unexpected error occurred while processing the request."
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
          schema:
            type: object
            properties:
              company:
                type: string
                description: The production company.
                example: Pixar Animation Studios
              count:
                type: integer
                description: The number of people (cast or crew) involved in movie production from that production company.
                example: 205
              percentage:
                type: number
                format: float
                description: The percentage of male, female and undefined that have worked in movie productions produced in that country.
                example: 50.37777
              gender:
                type: number
                description: The gender of the person (cast or crew) in the movie production. 1 = female, 2 = male, 0 = undefined.
                example: 2 
        500:
          description: An unexpected error occurred while processing the request.
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message.
                example: "An unexpected error occurred while processing the request."
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
          schema:
            type: object
            properties:
              genre:
                type: string
                description: The movie genre.
                example: Romance
              count:
                type: integer
                description: The number of people (cast or crew) involved in movie production from that movie genre.
                example: 401
              percentage:
                type: number
                format: float
                description: The percentage of male, female and undefined that have worked in movie productions produced in that country.
                example: 20.4222
              gender:
                type: number
                description: The gender of the person (cast or crew) in the movie production. 1 = female, 2 = male, 0 = undefined.
                example: 1
        500:
          description: An unexpected error occurred while processing the request.
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message.
                example: "An unexpected error occurred while processing the request."
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
          description: Gender distribution statistics by department (e.g. Directing, Acting).
          schema:
            type: object
            properties:
              department:
                type: string
                description: The department.
                example: Directing
              count:
                type: integer
                description: The number of people (cast or crew) involved in movie production from that department.
                example: 175
              percentage:
                type: number
                format: float
                description: The percentage of male, female and undefined from that department.
                example: 10.37777
              gender:
                type: number
                description: The gender of the person (cast or crew) in the movie production. 1 = female, 2 = male, 0 = undefined.
                example: 1 
        500:
          description: An unexpected error occurred while processing the request.
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message.
                example: "An unexpected error occurred while processing the request."
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
          description: Gender distribution statistics by movie production year fetched successfully.
          schema:
            type: object
            properties:
              year:
                type: number
                description: The movie production year.
                example: 1995
              count:
                type: integer
                description: The number of people (cast or crew) involved in movie production from that production year.
                example: 560
              percentage:
                type: number
                format: float
                description: The percentage of male, female and undefined that have worked in movie productions produced that year.
                example: 20.37777
              gender:
                type: number
                description: The gender of the person (cast or crew) in the movie production. 1 = female, 2 = male, 0 = undefined.
                example: 1
        500:
          description: An unexpected error occurred while processing the request.
          schema:
            type: object
            properties:
              message:
                type: string
                description: Error message.
                example: "An unexpected error occurred while processing the request."
      """
      return controller.get_gender_statistics_by_year()
    
    return gender_statistics_blueprint
  