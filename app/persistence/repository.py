import sys
import os
import json

from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)
    
    def get_all(self):
        return list(self._storage.values())
    
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return [obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value]
    

class InFileRepository(InMemoryRepository):

    def __init__(self, file_name):
        self.path = f"/root/Holbertonschool_New_Hbnb/app/data/{file_name}"
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
        # Convert datetime fields from ISO format strings back to datetime objects
        if 'created_at' in obj_data:
            obj_data['created_at'] = datetime.fromisoformat(obj_data['created_at'])
        if 'updated_at' in obj_data:
            obj_data['updated_at'] = datetime.fromisoformat(obj_data['updated_at'])

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
        with open(self.path, "w") as data_file:
            json.dump({obj_id: obj.to_dict() for obj_id, obj in self._storage.items()}, data_file, indent=4)
        print("Data has been saved")
    
    def add(self, obj):
        self._storage[obj.id] = obj
        self.save_to_file()
    
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            self.save_to_file()

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            self.save_to_file()
