import mongoengine as m_engine
import validators
from flask_bcrypt import generate_password_hash, check_password_hash
from .BaseSchema import BaseDocument

# Defines the schema for the User collection
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
            raise m_engine.ValidationError("First name is required and cannot be empty.")
        
        # Validate last_name
        if not self.last_name or not self.last_name.strip():
            raise m_engine.ValidationError("Last name is required and cannot be empty.")
        
        # Validate username
        if not self.username or not self.username.strip():
            raise m_engine.ValidationError("Username is required and cannot be empty.")
        
        # Validate email
        if not validators.email(self.email):
            raise m_engine.ValidationError("Invalid email address.")
        
        # Validate password
        if not self.password or len(self.password) < 8:
            raise m_engine.ValidationError("Password is required and must be at least 8 characters long.")

    # Save the user to the database
    def save(self, *args, **kwargs):
        if not self.password.startswith('$2b$'):
            self.set_password(self.password)
        return super(User, self).save(*args, **kwargs)