import pandas as pandas

# extract data from ratings_small, movies_metadata, and credits CSV files
def extract_csv():
    ratings_small = pandas.read_csv("movie_data/ratings_small.csv").to_dict('records')
    movies_metadata = pandas.read_csv("movie_data/movies_metadata.csv").to_dict('records')
    credits_data = pandas.read_csv("movie_data/credits.csv").to_dict('records')

    return ratings_small, movies_metadata, credits_data
  
ratings_small, movies_metadata, credits_data = extract_csv()

#prints for testing
# print('ratings ', ratings_small[0])
# print('movies ', movies_metadata[0])
# print('credits ', credits_data[0])