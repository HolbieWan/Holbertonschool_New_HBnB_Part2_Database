"""
User model for representing application users.

This module includes the `User` class, which defines the attributes, methods,
and validations associated with users in the application.
"""

from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError
from app.extensions import bcrypt, db


class User(BaseModel):
    """
    User model that represents application users.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address, unique per user.
        password (str): Hashed password for user authentication.
        is_admin (bool): Flag indicating if the user has admin privileges.
        places (list): List of places associated with the user.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.Column(db.JSON, default=[])

    def __init__(
            self,
            first_name,
            last_name,
            email,
            password,
            is_admin=False,
            places=None):
        """Initialize a new user instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = places if places is not None else []

    def hash_password(self, password):
        """
        Hashes the user's password before storing it.

        Args:
            password (str): The password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verifies if the provided password matches the stored hashed password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    def is_valid(self):
        """
        Validates the user data.

        Returns:
            bool: True if validation passes, otherwise raises ValueError.
        """
        try:
            if not all(
                isinstance(
                    attr,
                    str) for attr in [
                    self.email,
                    self.first_name,
                    self.last_name,
                    self.password]):
                raise TypeError(
                    "email, password, first_name, \
                    and last_name must be strings.")

            if not (
                0 < len(
                    self.first_name) <= 50) or not (
                0 < len(
                    self.last_name) <= 50):
                raise ValueError(
                    "first_name and last_name must not be empty \
                    and should be less than 50 characters.")

            validate_email(self.email)

        except TypeError as te:
            raise ValueError(f"Type error: {str(te)}")
        except EmailNotValidError as e:
            raise ValueError(f"Email validation failed: {str(e)}")
        except ValueError as ve:
            raise ValueError(f"Value error: {str(ve)}")

        return True

    def to_dict(self):
        """
        Converts the user instance to a dictionary.

        Returns:
            dict: A dictionary representation of the user instance.
        """
        return {
            "type": "user",
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
            "places": self.places,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
