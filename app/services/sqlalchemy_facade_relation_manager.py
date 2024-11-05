# sqlalchemy_facade_relation_manager.py

from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository


class SQLAlchemyFacadeRelationManager:
    def __init__(self, user_facade, place_facade, amenity_facade, review_facade):
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade

# User - place relations
# <------------------------------------------------------------------------>

    def create_place_for_user(self, user_id, place_data):
        user = self.user_facade.user_repo.get(user_id)
        
        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        place_data['owner_id'] = user_id
        place_data['owner_first_name'] = user.first_name

        place = self.place_facade.create_place(place_data)

        if isinstance(self.user_facade.user_repo, SQLAlchemyRepository):
            place_instance = self.place_facade.place_repo.get(place['id'])
            
            user.places.append(place_instance)
            db.session.commit()

        return place
