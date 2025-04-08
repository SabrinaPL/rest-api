import mongoengine as m_engine
from mongoengine import Document

class DBRepo:
    def __init__(self, model: Document, logger):
        """
        Initialize the repository with a specific model.
        :param model: The MongoEngine model to operate on.
        :param user_model: The MongoEngine model for user operations.
        """
        self.model = model
        self.logger = logger

    def find_by_id(self, object_id):
        """
        Find a document by its ID.
        :param object_id: The ID of the document.
        :return: The document or None if not found.
        """
        return self.model.objects(id=object_id).first()

    def find_all(self, **filters):
        """
        Find all documents matching the given filters.
        :param filters: Query filters as keyword arguments.
        :return: A queryset of matching documents.
        """
        return self.model.objects(**filters)

    def create(self, **kwargs):
        """
        Create a new document.
        :param kwargs: Fields and values for the new document.
        :return: The created document.
        """
        document = self.model(**kwargs)
        document.save()
        return document

    def update(self, object_id, **kwargs):
        """
        Update a document by its ID.
        :param object_id: The ID of the document to update.
        :param kwargs: Fields and values to update.
        :return: The number of documents updated (0 or 1).
        """
        return self.model.objects(id=object_id).update_one(**kwargs)

    def delete(self, object_id):
        """
        Delete a document by its ID.
        :param object_id: The ID of the document to delete.
        :return: The number of documents deleted (0 or 1).
        """
        return self.model.objects(id=object_id).delete()
    
    def find_by_field(self, field_name, value):
        """
        Find document(s) by a specific field and value.
        :param field_name: The name of the field to query.
        :param value: The value to match.
        :return: The document(s) or None if not found.
        """
        try:
            return self.model.objects(
                m_engine.Q(**{field_name: value})
            ) # Return all matching documents
        except Exception as e:
            self.logger.error(f"Error finding document by field {field_name}: {e}")
            return None
        
    def find_by_query(self, query):
        """
        Find document(s) by a specific query.
        :param query: The query to execute.
        :return: The document(s) or None if not found.
        """
        try:
            return self.model.objects(**query)
        except Exception as e:
            self.logger.error(f"Error finding document by query {query}: {e}")
            return self.model.objects.none()
