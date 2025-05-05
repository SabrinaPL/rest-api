import mongoengine as m_engine
from mongoengine import Document
from utils.CustomErrors import CustomError
from utils.custom_status_codes import GENERAL_CUSTOM_STATUS_CODES

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
        try:
            return self.model.objects(id=object_id).first()
        except Exception as e:
            self.logger.error(f"Error finding document by ID {object_id}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def find_all(self, **filters):
        """
        Find all documents matching the given filters.
        :param filters: Query filters as keyword arguments.
        :return: A queryset of matching documents.
        """
        try:
            return self.model.objects(**filters)
        except Exception as e:
            self.logger.error(f"Error finding documents with filters {filters}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def create(self, **kwargs):
        """
        Create a new document.
        :param kwargs: Fields and values for the new document.
        :return: The created document.
        """
        try:
            document = self.model(**kwargs)
            document.save()
            return document
        except Exception as e:
            self.logger.error(f"Error creating document with data {kwargs}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def update(self, object_id, **kwargs):
        """
        Update a document by its ID.
        :param object_id: The ID of the document to update.
        :param kwargs: Fields and values to update.
        :return: The number of documents updated (0 or 1).
        """
        try:
            return self.model.objects(id=object_id).update_one(**kwargs)
        except Exception as e:
            self.logger.error(f"Error updating document with ID {object_id}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def delete(self, object_id):
        """
        Delete a document by its ID.
        :param object_id: The ID of the document to delete.
        :return: The number of documents deleted (0 or 1).
        """
        try:
            return self.model.objects(id=object_id).delete()
        except Exception as e:
            self.logger.error(f"Error deleting document with ID {object_id}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
    
    def find_by_field(self, field_name, value):
        """
        Find document by a specific field and value.
        :param field_name: The name of the field to query.
        :param value: The value to match.
        """
        try:
            return self.model.objects(
                m_engine.Q(**{field_name: value})
            ).first() # Use first() to get a single document
        except Exception as e:
            self.logger.error(f"Error finding document by field {field_name}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
        
    def find_all_by_field(self, field_name, value):
        """
        Find documents by a specific field and value.
        :param field_name: The name of the field to query.
        :param value: The value to match.
        """
        try:
            return self.model.objects(
                m_engine.Q(**{field_name: value})
            )
        except Exception as e:
            self.logger.error(f"Error finding documents by field {field_name}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)

    def find_by_query(self, query):
        """
        Find document(s) by a specific query.
        :param query: The query to execute.
        """
        try:
            return self.model.objects(**query)
        except Exception as e:
            self.logger.error(f"Error finding document by query {query}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
        
    def find_by_query_with_pagination(self, query, page=1, per_page=100):
        """
        Find documents by a specific query with pagination.
        :param query: The query to execute.
        :param page: The page number (default is 1).
        :param per_page: The number of documents per page (default is 100).
        """
        try:
            # Calculate the number of documents to skip (as suggested by copilot)
            skip_count = (page - 1) * per_page

            return self.model.objects(**query).skip(skip_count).limit(per_page)
        except Exception as e:
            self.logger.error(f"Error finding documents by query {query} with pagination: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
        
    def create_indexes(self, fields, **kwargs):
        """
        Create indexes on the specified fields.
        :param fields: List of fields to index.
        :param kwargs: Additional options for index creation.
        """
        try:
            collection = self.model._get_collection()
            collection.create_index(fields, **kwargs)
            self.logger.info(f"Indexes created on fields: {fields}")
        except Exception as e:
            self.logger.error(f"Error creating indexes on fields {fields}: {e}")
            raise CustomError(GENERAL_CUSTOM_STATUS_CODES[500]["internal_error"], 500)
