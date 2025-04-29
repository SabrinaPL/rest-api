import mongoengine as m_engine
from .BaseSchema import BaseDocument

class GenderVisualizationData(BaseDocument):
    movie_id = m_engine.StringField(required=True)
    title = m_engine.StringField(required=False)
    year = m_engine.DateTimeField()
    countries = m_engine.ListField(m_engine.StringField(), required=True) # List of production countries
    companies = m_engine.ListField(m_engine.StringField(), required=False) # List of production companies
    genres = m_engine.ListField(m_engine.StringField(), required=False)
    department = m_engine.StringField(required=True) # Department of the person (e.g., acting, writing, directing, etc.)
    gender = m_engine.IntField(default=0)  # 0 = unknown, 1 = female, 2 = male
    name = m_engine.StringField(default="") # Name of the person (from the cast or crew)