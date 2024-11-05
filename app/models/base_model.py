# base_model.py
import uuid
from datetime import datetime

from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()
        if not self in db.session:
            db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if key in ['created_at', 'updated_at']:
                # Ensure the values are datetime objects
                if isinstance(value, str):
                    value = datetime.fromisoformat(value)
            if hasattr(self, key) and key not in ['id']:
                setattr(self, key, value)
        self.save()

