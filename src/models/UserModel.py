import mongoengine as m_engine
import validators
from flask_bcrypt import generate_password_hash, check_password_hash
from .BaseSchema import BaseDocument
from utils.CustomErrors import CustomError
from utils.custom_status_codes import ACCOUNT_CUSTOM_STATUS_CODES

# Defines the model for the User collection
class User(BaseDocument):
    first_name = m_engine.StringField(required=True)
    last_name = m_engine.StringField(required=True)
    username = m_engine.StringField(required=True, unique=True)
    email = m_engine.EmailField(required=True, unique=True)
    password = m_engine.StringField(required=True)

    # Hash the password before saving it to the database
    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Validate the user input before saving it to the database
    def clean(self):
        # Validate first_name
        if not self.first_name or not self.first_name.strip():
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["missing_first_name"], 400)
        
        if not isinstance(self.first_name, str):
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["invalid_first_name"], 400)
        
        # Validate last_name
        if not self.last_name or not self.last_name.strip():
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["missing_last_name"], 400)
        
        if not isinstance(self.last_name, str):
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["invalid_last_name"], 400)
        
        # Validate username
        if not self.username or not self.username.strip():
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["missing_username"], 400)
        
        if not isinstance(self.username, str):
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["invalid_username"], 400)
        
        # Validate email
        if not validators.email(self.email):
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["invalid_email"], 400)
        
        # Validate password
        if not self.password or len(self.password) < 8:
            raise CustomError(ACCOUNT_CUSTOM_STATUS_CODES[400]["invalid_password"], 400)

    # Save the user to the database
    def save(self, *args, **kwargs):
        if not self.password.startswith('$2b$'):
            self.set_password(self.password)
        return super(User, self).save(*args, **kwargs)