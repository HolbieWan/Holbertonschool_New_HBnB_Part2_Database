"""
BaseModel module providing a base class for models with common attributes
and methods for saving and updating instances.
"""

import uuid
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """
    A base class for all models in the application, containing common fields
    and methods for saving and updating instances.

    Attributes:
        id (str): Unique identifier for the instance.
        created_at (datetime): Timestamp of when the instance was created.
        updated_at (datetime): Timestamp of the last update.
    """
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    def __init__(self):
        """Initialize a new instance with a unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self, repo_type=None):
        """
        Save the object instance to the database or update its timestamps
        if using in-file storage.

        Args:
            repo_type (str): Type of repository ('sqlalchemyrepository'
                            for database, None for in-file storage).
        """
        if repo_type == 'sqlalchemy':
            self.updated_at = datetime.utcnow()
            if not db.session.contains(self):
                db.session.add(self)
            db.session.commit()
        else:
            if self.created_at is None:
                self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def update(self, data, repo_type=None):
        """
        Update the object's attributes based on a provided dictionary.

        Args:
            data (dict): Dictionary with new attribute values.
            repo_type (str): Type of repository ('sqlalchemy' for database,
                             None for in-file storage).

        Notes:
            - Fields 'id', 'created_at', and 'updated_at' are not updatable.
            - Converts 'created_at' and 'updated_at' from string to datetime
              for in-file storage.
        """
        for key, value in data.items():
            if hasattr(
                    self,
                    key) and key not in [
                    'id',
                    'created_at',
                    'updated_at']:
                setattr(self, key, value)
            elif key in ['created_at', 'updated_at'] \
                    and isinstance(value, str):
                setattr(self, key, datetime.fromisoformat(value))

        self.save(repo_type)
