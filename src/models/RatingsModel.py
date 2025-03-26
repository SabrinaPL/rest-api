import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the model for the Ratings collection
class Rating(BaseDocument):
    user_id = m_engine.IntField(required=True)
    movie_id = m_engine.IntField(required=True)
    rating = m_engine.FloatField(required=True)
    timestamp = m_engine.IntField(required=True)
