# Defines the model for the Movies collection
import mongoengine as m_engine
from .BaseSchema import BaseDocument

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

class MovieMetadata(BaseDocument):
    adult = m_engine.BooleanField(required=True)
    belongs_to_collection = m_engine.DictField()
    budget = m_engine.IntField(required=True)
    genres = m_engine.EmbeddedDocumentListField(Genre)
    homepage = m_engine.StringField()
    movie_id = m_engine.IntField(required=True, unique=True)
    imdb_id = m_engine.StringField()
    original_language = m_engine.StringField(required=True)
    original_title = m_engine.StringField(required=True)
    overview = m_engine.StringField()
    popularity = m_engine.FloatField()
    poster_path = m_engine.StringField()
    production_companies = m_engine.EmbeddedDocumentListField(ProductionCompany)
    production_countries = m_engine.EmbeddedDocumentListField(ProductionCountry)
    release_date = m_engine.DateTimeField()
    revenue = m_engine.IntField()
    runtime = m_engine.FloatField()
    spoken_languages = m_engine.EmbeddedDocumentListField(SpokenLanguage)
    status = m_engine.StringField()
    tagline = m_engine.StringField()
    title = m_engine.StringField(required=True)
    video = m_engine.BooleanField(required=True)
    vote_average = m_engine.FloatField()
    vote_count = m_engine.IntField()