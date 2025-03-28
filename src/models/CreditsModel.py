import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the model for the Credits collection
class Cast(m_engine.EmbeddedDocument):
    cast_id = m_engine.IntField(default=None)
    character = m_engine.StringField(default="")
    credit_id = m_engine.StringField(default="")
    gender = m_engine.IntField(default=None)
    id = m_engine.IntField(default=None)
    name = m_engine.StringField(default="")
    order = m_engine.IntField(default=None)
    profile_path = m_engine.StringField(default="")

class Crew(m_engine.EmbeddedDocument):
    credit_id = m_engine.StringField(default="")
    department = m_engine.StringField(default="")
    gender = m_engine.IntField(default=None)
    id = m_engine.IntField(default=None)
    job = m_engine.StringField(default="")
    name = m_engine.StringField(default="")
    profile_path = m_engine.StringField(default="")

class Credit(BaseDocument):
    id = m_engine.StringField(primary_key=True)
    cast = m_engine.EmbeddedDocumentListField(Cast, default=list)
    crew = m_engine.EmbeddedDocumentListField(Crew, default=list)