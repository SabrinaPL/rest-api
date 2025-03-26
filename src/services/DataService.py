from models.MovieModel import MovieMetadata, Genre, ProductionCompany, ProductionCountry, SpokenLanguage
from models.RatingsModel import Rating
from models.CreditsModel import Credit, Cast, Crew

# Service to save extracted movie data to the database
class DataService:
    def save_movies(self, movies_metadata):
        for movie in movies_metadata:
            movie_doc = MovieMetadata(
                adult=movie['adult'],
                belongs_to_collection=movie['belongs_to_collection'],
                budget=movie['budget'],
                genres=[Genre(**genre) for genre in eval(movie['genres'])],
                homepage=movie['homepage'],
                movie_id=movie['id'],
                imdb_id=movie['imdb_id'],
                original_language=movie['original_language'],
                original_title=movie['original_title'],
                overview=movie['overview'],
                popularity=movie['popularity'],
                poster_path=movie['poster_path'],
                production_companies=[ProductionCompany(**company) for company in eval(movie['production_companies'])],
                production_countries=[ProductionCountry(**country) for country in eval(movie['production_countries'])],
                release_date=pd.to_datetime(movie['release_date']),
                revenue=movie['revenue'],
                runtime=movie['runtime'],
                spoken_languages=[SpokenLanguage(**language) for language in eval(movie['spoken_languages'])],
                status=movie['status'],
                tagline=movie['tagline'],
                title=movie['title'],
                video=movie['video'],
                vote_average=movie['vote_average'],
                vote_count=movie['vote_count']
            )
            movie_doc.save()

    def save_ratings(self, ratings_small):
        for rating in ratings_small:
            rating_doc = Rating(
                user_id=rating['userId'],
                movie_id=rating['movieId'],
                rating=rating['rating'],
                timestamp=rating['timestamp']
            )
            rating_doc.save()

    def save_credits(self, credits_data):
        for credit in credits_data:
            credit_doc = Credit(
                movie_id=credit['movie_id'],
                cast=[Cast(**cast) for cast in eval(credit['cast'])],
                crew=[Crew(**crew) for crew in eval(credit['crew'])]
            )
            credit_doc.save()