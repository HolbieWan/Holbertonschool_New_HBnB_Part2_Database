from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        self.places.append(place)    
    
    def is_valid(self):
        try:
            if not all(isinstance(attr, str) for attr in [self.email, self.first_name, self.last_name, self.password]):
                raise TypeError("email, password, first_name, and last_name must be strings.")

            if not (0 < len(self.first_name) <= 50) or not (0 < len(self.last_name) <= 50):
                raise ValueError("first_name and last_name must not be empty and should be less than 50 characters.")

            validate_email(self.email)

        except TypeError as te:
            raise ValueError(f"Type error: {str(te)}")
        except EmailNotValidError as e:
            raise ValueError(f"Email validation failed: {str(e)}")
        except ValueError as ve:
            raise ValueError(f"Value error: {str(ve)}")
        
        return True

    def to_dict(self):
        return {
            "type": "user",
            "id" : self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "email" : self.email,
            "password" : self.password,
            "is_admin" : self.is_admin,
            "places" : self.places,
            "created_at" : self.created_at.isoformat(),
            "updated_at" : self.updated_at.isoformat()
        }
