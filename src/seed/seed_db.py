from seed.extract_csv import extract_csv

# Seed the database with extracted movie data
def seed_database(data_service, logger):
    ratings_small, movies_metadata, credits_data = extract_csv()
    try:
      # Save extracted movie data to the database
      logger.info("Seeding movies...")
      data_service.save_movies(movies_metadata)
      logger.info("Movies seeded successfully")
      logger.info("Seeding ratings...")
      data_service.save_ratings(ratings_small)
      logger.info("Ratings seeded successfully")
      logger.info("Seeding credits...")
      data_service.save_credits(credits_data)

      logger.info('Database seeded successfully')
      
    except Exception as e:
      logger.error(f"Error seeding database: {e}")
      raise

if __name__ == "__main__":
    seed_database()