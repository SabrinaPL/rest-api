import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the model for the Ratings collection
class Rating(BaseDocument):
    user_id = m_engine.IntField(required=True)
    movie_id = m_engine.IntField(required=True)
    rating = m_engine.FloatField(default=0.0, min_value=0.0, max_value=10.0)
    timestamp = m_engine.IntField(default=None)
