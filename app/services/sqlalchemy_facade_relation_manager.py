# sqlalchemy_facade_relation_manager.py

from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository
from sqlalchemy.orm import load_only
from app.models.user import User


class SQLAlchemyFacadeRelationManager:
    def __init__(self, user_facade, place_facade, amenity_facade, review_facade):
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade

# User - place relations
# <------------------------------------------------------------------------>

    def create_place_for_user(self, user_id, place_data):
        print("Using SQLAlchemyFacadeRelationManager to create place for user")
        user = self.user_facade.user_repo.get(user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        place_data['owner_id'] = user_id
        place_data['owner_first_name'] = user.first_name

        place = self.place_facade.create_place(place_data)
        place_id = place['id']  # Retrieve the new place's ID

        # Ensure user.places is initialized
        if user.places is None:
            user.places = []

        # Append only if the place_id is not already in the list
        if place_id not in user.places:
            user.places = user.places + [place_id]  # Reassign with a new list including the new place ID

        print(f"user.places before commit: {user.places}")
        db.session.add(user)  # Mark as modified for SQLAlchemy
        db.session.commit()

        print(f"user.places after commit: {user.places}")
        return place

#       <---------------------------------------------------------->


    def delete_place_from_owner_place_list(self, place_id, user_id):
        print("Using SQLAlchemyFacadeRelationManager to delete place for user")

        try:
            user = self.user_facade.user_repo.get(user_id)
            
            print(f"user.places before removal: {user.places}")

            if not user:
                raise ValueError(f"User with id: {user_id} not found")

            if place_id in user.places:
                user.places = [pid for pid in user.places if pid != place_id]
                print(f"user.places before removal: {user.places}")

                db.session.add(user)
                db.session.commit()
            else:
                raise ValueError(f"Place ID {place_id} not found in user's places list.")
            
            self.place_facade.place_repo.delete(place_id)

        except ValueError as e:
            print(str(e))

#       <---------------------------------------------------------->

 #  Place - Amenity relations
 # <------------------------------------------------------------------------>

    def add_amenity_to_a_place(self, place_id, amenity_data):
        place = self.place_facade.place_repo.get(place_id)
        amenity_name = amenity_data["name"]
        amenity = self.amenity_facade.amenity_repo.get_by_attribute("name",amenity_name)

        if not place:
            raise ValueError(f"Place: {place_id} not found.")

        if not amenity_data["name"] in place.amenities:
            # place.amenities.append(amenity_data['name'])
            place.amenities = place.amenities + [amenity_data["name"]]
            print(f"place.amenities before commit: {place.amenities}")
            # self.place_facade.place_repo.update(place_id, place.to_dict())
            db.session.add(place)
            db.session.commit()
            print(f"Amenity: {amenity_data['name']} has been added to the place: {place_id}")

            if not amenity:
                amenity = self.amenity_facade.create_amenity(amenity_data)

        else:
            raise ValueError(f"Amenity: {amenity_data['name']} already exist for this place: {place_id}")

        return amenity

            # <------------------------------------------>

    def delete_amenity_from_place_list(self, amenity_name, place_id):
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")

        if amenity_name in place.amenities:
            place.amenities = [amty_name for amty_name in place.amenities if  amty_name != amenity_name]
            print(f"place.amenities before commit: {place.amenities}")
            db.session.add(place)
            db.session.commit()
            print(f"place.amenities after commit: {place.amenities}")
        else:
            raise ValueError(f"Amenity {amenity_name} not found in places_amenities list.")


# #  Place - review relations
# # <------------------------------------------------------------------------>

    def create_review_for_place(self, place_id, user_id, review_data):
        place = self.place_facade.place_repo.get(place_id)
        user = self.user_facade.user_repo.get(user_id)
    
        if not place:
            raise ValueError(f"Place with id {place_id} not found.")
        
        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        review_data["place_id"] = place_id
        review_data["place_name"] = place.title
        review_data["user_first_name"] = user.first_name
        review_data["user_id"] = user_id

        review = self.review_facade.create_review(review_data)
        review_id = review['id']

        if place.reviews is None:
            place.reviews = []

        if review_id not in place.reviews:
            place.reviews = place.reviews + [review_id]

        print(f"place.reviews before commit: {place.reviews}")
        db.session.add(place)
        db.session.commit()
        print(f"place.reviews after commit: {place.reviews}")

        return review

            # <------------------------------------------>

    def delete_review_from_place_list(self, review_id, place_id):
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")
        
        reviews = place.reviews

        if review_id in reviews:
            place.reviews = [rev_id for rev_id in reviews if rev_id != review_id]
            print(f"place.reviews before commit: {place.reviews}")
            db.session.add(place)
            db.session.commit()
            print(f"place.reviews after commit: {place.reviews}")
        else:
            raise ValueError(f"Review with id: {review_id} not found")

        self.review_facade.review_repo.delete(review_id)