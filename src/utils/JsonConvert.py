from bson import json_util
import json

class JsonConvert:
    def __init__(self, logger):
        self.logger = logger
        pass
    
    def serialize_document(self, document):
        """Convert a MongoEngine document to JSON."""
        if document is None:
            return None
        # Convert the document to a dictionary
        document_dict = document.to_mongo().to_dict()
        # Convert the dictionary to a JSON string
        return json.loads(json_util.dumps(document_dict))

    def serialize_documents(self, documents):
        self.logger.info("Serializing documents to JSON")
        """Convert a list of MongoEngine documents to JSON."""
        return [self.serialize_document(doc) for doc in documents]
