import pandas as pandas
import ast as ast
import uuid
from models.MovieModel import MovieMetaData
from models.RatingsModel import Rating
from models.CreditsModel import Credit, Cast, Crew

# Service to save extracted movie data to the database
class DataService:
    def __init__(self, logger):
        self.logger = logger
    
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
            return {"message": "Internal server error"}, 500

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

    def save_credits(self, credits_data):    
        for credit in credits_data[:10000]:  # Limit to 10000 credits for performance
            # Validate credit ID
            id = credit.get('id')
            
            print(f"Processing credit with ID: {id}")
            
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
                
    def save_gender_data(self, movies_metadata, credits_data):
        # Create a movie lookup dictionary for optimization (as suggested by chatGPT)
        movie_lookup = {}
        
        for movie in movies_metadata:
            # Extract movie Id, title, production countries, production companies
            
        for credit in credits_data:
            # Extract cast and crew data, connect to movie data, extract department, gender and name
 
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