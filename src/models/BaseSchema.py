import mongoengine as m_engine
import datetime

# BaseDocument class to be inherited by other models
class BaseDocument(m_engine.Document):
    meta = {'abstract': True}
    # Stores timestamp of when document was created and updated, set to current UTC time
    created_at = m_engine.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = m_engine.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        # Checks that document is being created for the first time, sets created_at timestamp
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        # Sets updated_at timestamp to current time
        self.updated_at = datetime.datetime.utcnow()

        # Calls the save method of the parent class
        return super(BaseDocument, self).save(*args, **kwargs)