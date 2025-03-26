from utils.json_utils import to_json
from services.DataService import DataService
from seed.extract_csv import extract_csv

class DataController:
    def __init__(self, data_service):
        self.data_service = data_service

    def process_and_save_data(self):
        ratings_small, movies_metadata, credits_data = extract_csv()

        # Convert data to JSON format
        movies_metadata_json = to_json(movies_metadata)
        ratings_json = to_json(ratings_small)
        credits_json = to_json(credits_data)

        # Print for testing
        print(movies_metadata_json[0])

        # Save extracted movie data to the database
        self.data_service.save_movies(movies_metadata_json)
        self.data_service.save_ratings(ratings_json)
        self.data_service.save_credits(credits_json)

        # Print for testing
        print("Data saved to MongoDB")
