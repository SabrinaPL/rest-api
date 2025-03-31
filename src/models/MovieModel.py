import mongoengine as m_engine
from .BaseSchema import BaseDocument

# Defines the model for the Movies collection
class Genre(m_engine.EmbeddedDocument):
    id = m_engine.IntField(required=True)
    name = m_engine.StringField(required=True)

class ProductionCompany(m_engine.EmbeddedDocument):
    id = m_engine.IntField(required=True)
    name = m_engine.StringField(required=True)

class ProductionCountry(m_engine.EmbeddedDocument):
    iso_3166_1 = m_engine.StringField(required=True)
    name = m_engine.StringField(required=True)

class SpokenLanguage(m_engine.EmbeddedDocument):
    iso_639_1 = m_engine.StringField(required=True)
    name = m_engine.StringField(required=True)

class MovieMetaData(BaseDocument):
    movie_id = m_engine.StringField(required=True, unique=True)
    adult = m_engine.BooleanField(default=False)
    belongs_to_collection = m_engine.DictField(default={})
    budget = m_engine.IntField(default=0, min_value=0)
    genres = m_engine.ListField(m_engine.EmbeddedDocumentField(Genre), default=[])
    homepage = m_engine.StringField(default="")
    imdb_id = m_engine.StringField(default="")
    original_language = m_engine.StringField(default="")
    original_title = m_engine.StringField(default="")
    overview = m_engine.StringField(default="")
    popularity = m_engine.FloatField(default=0.0, min_value=0.0)
    poster_path = m_engine.StringField(default="")  # 
    production_companies = m_engine.ListField(m_engine.EmbeddedDocumentField(ProductionCompany), default=[])  
    production_countries = m_engine.ListField(m_engine.EmbeddedDocumentField(ProductionCountry), default=[])
    release_date = m_engine.DateTimeField()
    revenue = m_engine.IntField(default=0, min_value=0) 
    runtime = m_engine.IntField(default=0, min_value=0)
    spoken_languages = m_engine.ListField(m_engine.EmbeddedDocumentField(SpokenLanguage), default=[])
    status = m_engine.StringField(default="")
    tagline = m_engine.StringField(default="")
    title = m_engine.StringField(required=True)
    video = m_engine.BooleanField(default=False)
    vote_average = m_engine.FloatField(default=0.0, min_value=0.0, max_value=10.0)
    vote_count = m_engine.IntField(default=0, min_value=0)