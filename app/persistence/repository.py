"""
Repository module for managing data storage with support for in-memory,
file-based, and database repositories.
"""

import os
import json
from datetime import datetime
from abc import ABC, abstractmethod

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import db


class Repository(ABC):
    """Abstract base class for repository interfaces."""
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects in the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object with the given ID using the provided data."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve objects by a specific attribute."""
        pass

# <--------------------------------------------------------->


class InMemoryRepository(Repository):
    """In-memory repository for storing data without persistence."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to the in-memory storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID from in-memory storage."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects stored in-memory."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with the given ID using provided data."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object by its ID from in-memory storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve objects by a specific attribute value."""
        return [
            obj for obj in self._storage.values() if getattr(
                obj, attr_name) == attr_value]

# <--------------------------------------------------------->


class InFileRepository(InMemoryRepository):
    """File-based repository for persisting data in JSON format."""

    def __init__(self, file_name):

        self.path = (
            f"/root/Holbertonschool_New_HBnB_Part2_Database\
            /app/data/{file_name}"
        )
        self._storage = {}

        if not os.path.exists(self.path):
            with open(self.path, "w") as data_file:
                json.dump(self._storage, data_file)
            print(f"The file {self.path} has been created")
        else:
            print(f"The file {self.path} already exists")
            try:
                with open(self.path, "r") as data_file:
                    data = json.load(data_file)
                    self._storage = {
                        obj_id: self.dict_to_obj(obj_data)
                        for obj_id, obj_data in data.items()
                    }
            except (json.JSONDecodeError, ValueError):
                print("The file is empty or corrupted")

    def dict_to_obj(self, obj_data):
        """
        Convert a dictionary to an object, handling different model types and
        date fields.
        """
        if 'created_at' in obj_data:
            obj_data['created_at'] = datetime.fromisoformat(
                obj_data['created_at'])
        if 'updated_at' in obj_data:
            obj_data['updated_at'] = datetime.fromisoformat(
                obj_data['updated_at'])

        obj_type = obj_data.get('type')

        if obj_type == 'user':

            user = User(
                first_name=obj_data['first_name'],
                last_name=obj_data['last_name'],
                email=obj_data['email'],
                password=obj_data['password'],
                is_admin=obj_data['is_admin']
            )
            user.id = obj_data['id']
            user.created_at = obj_data['created_at']
            user.updated_at = obj_data['updated_at']
            user.places = obj_data['places']
            return user

        elif obj_type == 'place':

            place = Place(
                title=obj_data['title'],
                description=obj_data['description'],
                price=obj_data['price'],
                latitude=obj_data['latitude'],
                longitude=obj_data['longitude'],
                owner_first_name=obj_data['owner_first_name'],
                owner_id=obj_data['owner_id'],
                amenities=obj_data['amenities'],
                reviews=obj_data['reviews']
            )

            place.id = obj_data['id']
            place.created_at = obj_data['created_at']
            place.updated_at = obj_data['updated_at']
            return place

        elif obj_type == 'review':

            review = Review(
                text=obj_data['text'],
                rating=obj_data['rating'],
                place_id=obj_data['place_id'],
                place_name=obj_data['place_name'],
                user_id=obj_data['user_id'],
                user_first_name=obj_data['user_first_name']
            )

            review.id = obj_data['id']
            review.created_at = obj_data['created_at']
            review.updated_at = obj_data['updated_at']
            return review

        elif obj_type == 'amenity':

            amenity = Amenity(name=obj_data['name'])
            amenity.id = obj_data['id']
            amenity.created_at = obj_data['created_at']
            amenity.updated_at = obj_data['updated_at']
            return amenity

        else:
            raise ValueError(f"Unknown object type: {obj_type}")

    def save_to_file(self):
        """Persist data in storage to the JSON file."""
        with open(self.path, "w") as data_file:
            json.dump({obj_id: obj.to_dict() for obj_id,
                      obj in self._storage.items()}, data_file, indent=4)
        print("Data has been saved")

    def add(self, obj):
        """Add an object to the file storage and save to file."""
        self._storage[obj.id] = obj
        self.save_to_file()

    def update(self, obj_id, data):
        """Update an object in file storage and save to file."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            self.save_to_file()

    def delete(self, obj_id):
        """Delete an object from file storage and save to file."""
        if obj_id in self._storage:
            del self._storage[obj_id]
            self.save_to_file()

# <--------------------------------------------------------->


class SQLAlchemyRepository(Repository):
    """Database repository for persisting data in DB using SQLAlchemy ORM."""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add an object to the database."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its ID from the database."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects of this model from the database."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object in the database with the given data."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            db.session.commit()

    def delete(self, obj_id):
        """Delete an object by its ID from the database."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve objects by a specific attribute from the database."""
        return self.model.query.filter_by(**{attr_name: attr_value}).all()
