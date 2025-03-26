import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the model for the Credits collection
class Cast(m_engine.EmbeddedDocument):
    cast_id = m_engine.IntField(required=True)
    character = m_engine.StringField(required=True)
    credit_id = m_engine.StringField(required=True)
    gender = m_engine.IntField()
    id = m_engine.IntField(required=True)
    name = m_engine.StringField(required=True)
    order = m_engine.IntField()

class Crew(m_engine.EmbeddedDocument):
    credit_id = m_engine.StringField(required=True)
    department = m_engine.StringField(required=True)
    gender = m_engine.IntField()
    id = m_engine.IntField(required=True)
    job = m_engine.StringField(required=True)
    name = m_engine.StringField(required=True)

class Credit(BaseDocument):
    movie_id = m_engine.IntField(required=True, unique=True)
    cast = m_engine.EmbeddedDocumentListField(Cast)
    crew = m_engine.EmbeddedDocumentListField(Crew)