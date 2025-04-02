from mongoengine import Document

class DBRepo:
    def __init__(self, model: Document):
        """
        Initialize the repository with a specific model.
        :param model: The MongoEngine model to operate on.
        """
        self.model = model

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
        Find a document by a specific field and value.
        :param field_name: The name of the field to query.
        :param value: The value to match.
        :return: The document or None if not found.
        """
        return self.model.objects(**{field_name: value}).first()

    def find_by_username(self, username):
        """
        Find a user by username.
        :param username: The username to search for.
        :return: The user document or None if not found.
        """
        return self.find_by_field('username', username)
