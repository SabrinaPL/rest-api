import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the schema for the User collection
class User(BaseDocument):
    username = m_engine.StringField(required=True, unique=True)
    email = m_engine.EmailField(required=True, unique=True)
    password = m_engine.StringField(required=True)
