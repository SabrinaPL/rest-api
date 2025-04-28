from seed.extract_csv import extract_csv
from mongoengine import connection

# Check if DB has already been seeded with movie data
def is_db_seeded():
    db = connection.get_db()
    if (
        db["movie_meta_data"].count_documents({}) > 0 and
        db["rating"].count_documents({}) > 0 and
        db["credit"].count_documents({}) > 0
    ):
        return True
    else:
        return False

# Seed the database with extracted movie data
def seed_database(data_service, logger):
    # if is_db_seeded():
    #     logger.info("✅ Database already seeded, skipping seeding process.")
    #     return
    # else:
    logger.info("🚀 Seeding the database...")

    ratings_small, movies_metadata, credits_data = extract_csv()

    try:
      # Save extracted movie data to the database
      logger.info("🚀 Seeding movies...")
      # data_service.save_movies(movies_metadata)
      logger.info("🚀 Seeding ratings...")
      # data_service.save_ratings(ratings_small)
      logger.info("🚀 Seeding credits...")
      # data_service.save_credits(credits_data)
      logger.info("🚀 Seeding gender data...")
      data_service.save_gender_data(movies_metadata, credits_data)

      logger.info('✅ Database seeded successfully')
      
    except Exception as e:
      logger.error(f"❌ Error seeding database: {e}")
      raise e
