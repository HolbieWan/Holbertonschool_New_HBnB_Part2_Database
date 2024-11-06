# base_model.py
import uuid
from datetime import datetime

from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self, repo_type=None):
        """Save the object based on the repository type"""
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
        """Update the attributes of the object based on the provided dictionary and repo type"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
            elif key in ['created_at', 'updated_at'] and isinstance(value, str):
                # Convert string back to datetime if necessary for in-file storage
                setattr(self, key, datetime.fromisoformat(value))

        self.save(repo_type)

    # def save(self):
    #     """Update the updated_at timestamp whenever the object is modified"""
    #     self.updated_at = datetime.utcnow()
    #     if not self in db.session:
    #         db.session.add(self)
    #     db.session.commit()

    # def update(self, data):
    #     """Update the attributes of the object based on the provided dictionary"""
    #     for key, value in data.items():
    #         if key in ['created_at', 'updated_at']:
    #             # Ensure the values are datetime objects
    #             if isinstance(value, str):
    #                 value = datetime.fromisoformat(value)
    #         if hasattr(self, key) and key not in ['id']:
    #             setattr(self, key, value)
    #     self.save()

