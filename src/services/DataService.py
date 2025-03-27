import pandas as pandas
import ast as ast
from models.MovieModel import MovieMetadata
from models.RatingsModel import Rating
from models.CreditsModel import Credit, Cast, Crew

# Service to save extracted movie data to the database
class DataService:
    def __init__(self, logger):
        self.logger = logger
    
    def save_movies(self, movies_metadata):
        for movie in movies_metadata:
            # Validate movie ID
            try:
                movie_id = int(movie['id'])
            except (ValueError, TypeError):
                self.logger.warning(f"Invalid movie ID: {movie['id']}. Skipping...")
                continue

            # Check if the movie already exists
            if MovieMetadata.objects(movie_id=movie_id).first():
                self.logger.info(f"Skipping duplicate movie with ID: {movie_id}")
                continue

            try:
                movie_doc = MovieMetadata(
                    movie_id=movie_id,
                    adult=movie.get('adult', False),
                    belongs_to_collection=self.convert_to_dict(movie.get('belongs_to_collection')),
                    budget=movie.get('budget', 0),
                    genres=self.convert_to_list(movie.get('genres')),
                    homepage=self.safe_string(movie.get('homepage')),
                    imdb_id=self.safe_string(movie.get('imdb_id')),
                    original_language=self.safe_string(movie.get('original_language')),
                    original_title=self.safe_string(movie.get('original_title')),
                    overview=self.safe_string(movie.get('overview')),
                    popularity=movie.get('popularity', 0.0),
                    poster_path=self.safe_string(movie.get('poster_path')),
                    production_companies=self.convert_to_list(movie.get('production_companies')),
                    production_countries=self.convert_to_list(movie.get('production_countries')),
                    release_date=pandas.to_datetime(movie.get('release_date'), errors='coerce'),
                    revenue=movie.get('revenue', 0),
                    runtime=movie.get('runtime', 0),
                    spoken_languages=self.convert_to_list(movie.get('spoken_languages')),
                    status=self.safe_string(movie.get('status')),
                    tagline=self.safe_string(movie.get('tagline')),
                    title=self.safe_string(movie.get('title')),
                    video=movie.get('video', False),
                    vote_average=movie.get('vote_average', 0.0),
                    vote_count=movie.get('vote_count', 0)
                )
                movie_doc.save()
            except Exception as e:
                self.logger.error(f"Error saving movie with ID: {movie_id}. Error: {e}")

    def save_ratings(self, ratings_small):
        for rating in ratings_small:
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
        for credit in credits_data:
            
            movie_id = credit.get('movie_id')
            # Check if 'movie_id' is present in the credit data
            if not movie_id:
                self.logger.warning(f"Skipping credit data without movie_id: {credit}")
                continue
            
            # Check if the credit already exists
            if Credit.objects(movie_id=movie_id).first():
                self.logger.info(f"Skipping duplicate credit with movie ID: {movie_id}")
                continue
            
            try:
                credit_doc = Credit(
                    movie_id=movie_id,
                    cast=[Cast(**cast) for cast in self.convert_to_list(credit.get('cast', [])) if cast.get('id')],
                    crew=[Crew(**crew) for crew in self.convert_to_list(credit.get('crew', [])) if crew.get('id')]
                )
                credit_doc.save()
            except Exception as e:
                self.logger.error(f"Error saving credit with movie ID: {movie_id}. Error: {e}")
 
    def convert_to_dict(self, value):
        if isinstance(value, str):
            try:
                # ast.literal_eval() used since it will evaluate without executing code (lowers the risk of code injection)
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