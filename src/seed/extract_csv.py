# extract ratings_small, movies_metadata, and credits CSV files

import pandas as pandas

def extract_csv():
    ratings_small = pandas.read_csv("movie_data/ratings_small.csv").to_dict('records')
    movies_metadata = pandas.read_csv("movie_data/movies_metadata.csv").to_dict('records')
    credits_data = pandas.read_csv("movie_data/credits.csv").to_dict('records')

    return ratings_small, movies_metadata, credits_data
  
ratings_small, movies_metadata, credits_data = extract_csv()

print(movies_metadata[0])

# process the extracted data after creating the data models for the database, with mongoEngine (classes for each collection)

