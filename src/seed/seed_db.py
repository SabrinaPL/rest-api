from seed.extract_csv import extract_csv

# Seed the database with extracted movie data
def seed_database(data_service):
    print('seeding database')
    print('data_service instance in seed file', data_service)

    ratings_small, movies_metadata, credits_data = extract_csv()

    # Save extracted movie data to the database
    data_service.save_movies(movies_metadata)
    data_service.save_ratings(ratings_small)
    data_service.save_credits(credits_data)

    print("Database seeded successfully")

if __name__ == "__main__":
    seed_database()