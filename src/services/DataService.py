import pandas as pandas
import ast as ast
import uuid
import math
from models.MovieModel import MovieMetaData
from models.RatingsModel import Rating
from models.CreditsModel import Credit, Cast, Crew
from models.GenderDataModel import GenderStatistics
from utils.custom_status_codes import GENERAL_CUSTOM_STATUS_CODES
from utils.CustomErrors import CustomError

# Service to save extracted movie data to the database
class DataService:
    def __init__(self, logger, gender_data_db_repo):
        self.logger = logger
        self.gender_data_db_repo = gender_data_db_repo
    
    def save_movies(self, movies_metadata):
        for movie in movies_metadata[:10000]:  # Limit to 10000 movies for performance

            # Validate movie ID
            try:
                movie_id = str(movie['id'])
            except (ValueError, TypeError):
                self.logger.warning(f"Invalid movie ID: {movie['id']}. Skipping...")
                continue

            # Check if the movie already exists
            if MovieMetaData.objects(movie_id=movie_id).first():
                self.logger.info(f"Skipping duplicate movie with ID: {movie_id}")
                continue

            try:
                # Preprocess fields to handle invalid values (as suggested by copilot)
                runtime = movie.get('runtime', 0)
                runtime = int(runtime) if not pandas.isna(runtime) else 0
                
                release_date = pandas.to_datetime(movie.get('release_date'), errors='coerce')
                release_date = release_date if not pandas.isna(release_date) else None
                
                revenue = movie.get('revenue', 0)
                revenue = int(revenue) if not pandas.isna(revenue) and revenue is not None else 0
                
                vote_count = movie.get('vote_count', 0)
                vote_count = int(vote_count) if not pandas.isna(vote_count) and vote_count is not None else 0
                
                budget = movie.get('budget', 0)
                budget = int(budget) if not pandas.isna(budget) and isinstance(budget, (int, float)) else 0
                
                belongs_to_collection = self.convert_to_dict(movie.get('belongs_to_collection'))
                
                production_companies = self.convert_to_list(movie.get('production_companies'))
                production_countries = self.convert_to_list(movie.get('production_countries'))
                
                movie_doc = MovieMetaData(
                    movie_id=movie_id,
                    adult=movie.get('adult', False),
                    belongs_to_collection=belongs_to_collection,
                    budget=budget,
                    genres=self.convert_to_list(movie.get('genres')),
                    homepage=self.safe_string(movie.get('homepage')),
                    imdb_id=self.safe_string(movie.get('imdb_id')),
                    original_language=self.safe_string(movie.get('original_language')),
                    original_title=self.safe_string(movie.get('original_title')),
                    overview=self.safe_string(movie.get('overview')),
                    popularity=movie.get('popularity', 0.0),
                    poster_path=self.safe_string(movie.get('poster_path')),
                    production_companies=production_companies,
                    production_countries=production_countries,
                    release_date=release_date,
                    revenue=revenue,
                    runtime=runtime,
                    spoken_languages=self.convert_to_list(movie.get('spoken_languages')),
                    status=self.safe_string(movie.get('status')),
                    tagline=self.safe_string(movie.get('tagline')),
                    title=self.safe_string(movie.get('title')),
                    video=movie.get('video', False),
                    vote_average=movie.get('vote_average', 0.0),
                    vote_count=vote_count
                )
                movie_doc.save()
            except Exception as e:
                self.logger.error(f"Error saving movie with ID: {movie_id}. Error: {e}")
                raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
            
    def save_new_movie(self, movie_data):
        self.logger.info("Saving new movie to the database")

        # Generate a new unique ID for the movie (as suggested by copilot)
        movie_data['id'] = self.generate_unique_id()
        self.logger.info(f"Generated new unique ID for movie: {movie_data['id']}")

        try:
            # Preprocess fields to handle invalid values (as suggested by copilot)
            release_date = pandas.to_datetime(movie_data.get('release_date'), errors='coerce')
            release_date = release_date if not pandas.isna(release_date) else None
            
            genres = self.convert_to_list(movie_data.get('genres'))
            
            # Create the new movie document
            movie_doc = MovieMetaData(
                movie_id=movie_data['id'],
                title=self.safe_string(movie_data.get('title')),
                release_date=release_date,
                genres=genres,
                overview=self.safe_string(movie_data.get('overview')),
            )

            movie_doc.save()
            self.logger.info(f"Movie with ID {movie_data['id']} saved successfully")
            
            return str(movie_doc.id)
            
        except Exception as e:
            self.logger.error(f"Error saving movie with ID: {movie_data['id']}. Error: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def save_ratings(self, ratings_small):
        for rating in ratings_small[:10000]:  # Limit to 10000 ratings for performance
            # Validate user ID and movie ID
            user_id = rating.get('userId')
            movie_id = rating.get('movieId')
            if not user_id or not movie_id:
                self.logger.warning(f"Skipping rating data without user ID or movie ID: {rating}")
                continue

            try:
                rating_doc = Rating(
                    user_id=rating['userId'],
                    movie_id=rating['movieId'],
                    rating=rating['rating'],
                    timestamp=rating['timestamp']
                )
                rating_doc.save()
            except Exception as e:
                self.logger.error(f"Error saving rating with user ID: {user_id} and movie ID: {movie_id}. Error: {e}")
                raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def save_credits(self, credits_data):    
        for credit in credits_data[:10000]:  # Limit to 10000 credits for performance
            # Validate credit ID
            id = credit.get('id')
            
            self.logger.info(f"Processing credit with ID: {id}")
            
            if not id:
                self.logger.warning(f"Skipping credit data without ID: {credit}")
                continue

            try:
                id = str(id)
            except (ValueError, TypeError):
                self.logger.warning(f"Invalid ID: {id}. Skipping...")
                continue
     
            # Check if the credit already exists
            if Credit.objects(id=id).first():
                self.logger.info(f"Skipping duplicate credit with ID: {id}")
                continue

            try:
                credit_doc = Credit(
                    id=id,
                    cast=[Cast(**cast) for cast in self.convert_to_list(credit.get('cast', [])) if cast.get('id')],
                    crew=[Crew(**crew) for crew in self.convert_to_list(credit.get('crew', [])) if crew.get('id')]
                )
                credit_doc.save()
            except Exception as e:
                self.logger.error(f"Error saving credit with ID: {id}. Error: {e}")
                raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
                
    def save_gender_data(self, movies_metadata, credits_data):
        # Create a movie lookup dictionary for optimization (as suggested by chatGPT)
        movie_lookup = {}
        
        try:
            for movie in movies_metadata:
                movie_id = str(movie['id'])
                if not movie_id:
                    self.logger.warning(f"Skipping movie data without ID: {movie}")
                    continue

                # Preprocess release date (as suggested by copilot)
                release_date = pandas.to_datetime(movie.get('release_date'), errors='coerce')
                release_date = release_date if not pandas.isna(release_date) else None
                release_year = release_date.year if release_date else None
            
                movie_lookup[movie_id] = {
                    'title': self.safe_string(movie.get('title', '')),
                    'production_countries': self.extract_string_list(movie.get('production_countries'), 'iso_3166_1'),
                    'production_companies': self.extract_string_list(movie.get('production_companies'), 'name'),
                    'genres': self.extract_string_list(movie.get('genres'), 'name'),
                    'year': release_year
                }
  
            for credit in credits_data:
                movie_id = str(credit['id'])

                self.logger.info(f"Processing credit with movie ID: {movie_id}")
            
                if not movie_id or movie_id not in movie_lookup:
                    self.logger.warning(f"Skipping credit data without valid movie ID: {credit}")
                    continue
            
                movie_info = movie_lookup[movie_id]
                movie_title = movie_info['title']
                countries = movie_info['production_countries']
                companies = movie_info['production_companies']
                genres = movie_info['genres']
                year = movie_info['year']
            
                # This check is added to ensure that we have valid production countries before proceeding, since production countries are essential for gender data visualization and analysis
                if not countries:
                    self.logger.warning(f"Missing production countries for movie ID: {movie_id}. Skipping...")
                    continue

                cast_data = self.convert_to_list(credit.get('cast', []))
                crew_data = self.convert_to_list(credit.get('crew', []))
 
                for cast in cast_data:
                    self.logger.info(f"Processing cast data: {cast}")

                    name = cast.get('name')
                    gender = cast.get('gender')
                    department = 'Acting'
                
                    if gender is None:
                        self.logger.warning(f"Skipping cast data without valid gender: {cast}")
                        continue

                    gender_data_doc = GenderStatistics(
                        movie_id=movie_id,
                        title=movie_title,
                        year=year,
                        countries=countries,
                        companies=companies,
                        genres=genres,
                        department=department,
                        gender=gender,
                        name=name
                    )
                    gender_data_doc.save()

                for crew in crew_data:
                    name = crew.get('name')
                    department = crew.get('department')
                    gender = crew.get('gender')
                
                    if not department:
                        self.logger.warning(f"Skipping crew data without valid department: {crew}")
                        continue
                    if gender is None:
                        self.logger.warning(f"Skipping cast data without valid gender: {crew}")
                        continue
     
                    gender_data_doc = GenderStatistics(
                        movie_id=movie_id,
                        title=movie_title,
                        year=year,
                        countries=countries,
                        companies=companies,
                        genres=genres,
                        department=department,
                        gender=gender,
                        name=name
                    )
                    gender_data_doc.save()
        except Exception as e:
            self.logger.error(f"Error processing crew data. Error: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
        
    def create_indexes(self):
        """
        Create indexes for database collections to improve query performance.
        """
        try:
            # Index for map visualization (gender distribution by countries)
            self.gender_data_db_repo.create_indexes([("countries", 1), ("gender", 1)])
            
            # Index for distribution by department, movie genres, production companies and year (independent of countries)
            self.gender_data_db_repo.create_indexes([("department", 1), ("gender", 1)])
            self.gender_data_db_repo.create_indexes([("genres", 1), ("gender", 1)])
            self.gender_data_db_repo.create_indexes([("companies", 1), ("gender", 1)])
            self.gender_data_db_repo.create_indexes([("year", 1), ("gender", 1)])
            
            self.logger.info("✅ Compound indexes created successfully!")
        except Exception as e:
            self.logger.error(f"❌ Error creating indexes: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def convert_to_dict(self, value):
        if isinstance(value, str):
            try:
                # ast.literal_eval() used since it will evaluate without executing code (lowers the risk of code injection), as suggested by copilot
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return {} # Return an empty dictionary if the string is not a valid dictionary
        elif isinstance(value, dict):
            return value # Return the value if it is already a dictionary
        return {} # Return an empty dictionary if the value is not a string or dictionary

    def convert_to_list(self, value):
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return [] # Return an empty list if the string is not a valid list
        elif isinstance(value, list):
            return value # Return the value if it is already a list
        return [] # Return an empty list if the value is not a string or list

    def safe_string(self, value):
        if value is None or (isinstance(value, float)) and pandas.isna(value):
            return "" # Return an empty string if the value is None or NaN
        return str(value) if value else ""
    
    def generate_unique_id(self):
        while True:
            # Generate a random unique ID (e.g., UUID or custom logic)
            new_id = str(uuid.uuid4())
      
            if not MovieMetaData.objects(movie_id=new_id).first():
                self.logger.info(f"Generated unique ID: {new_id}")
                return new_id
            
    def extract_string_list(self, value, key='name'):
        """
        Extracts a list of strings from a given value. The key parameter allows customization of the extraction process.
        """
        self.logger.info(f"Extracting string list from value: {value} with key: {key}")

        # Sanitize bad input
        if value is None or isinstance(value, float) and math.isnan(value):
            return []

        try:
            items = self.convert_to_list(value)
            result = []

            for item in items:
                if isinstance(item, dict) and key in item:
                    result.append(str(item[key]))
                elif isinstance(item, (str, int)):
                    result.append(str(item))
                # skip floats, None, etc.
            
            self.logger.info(f"Extracted string list: {result}")

            return result
        except Exception as e:
            self.logger.error(f"Error extracting string list from value: {value}. Error: {e}")
            return []


