"""
sqlalchemy_facade_relation_manager.py

This module defines the SQLAlchemyFacadeRelationManager class, managing
relationships and interactions between User, Place, Amenity, and Review
entities in a database using SQLAlchemy. This class provides functionality
to handle operations like creating, deleting, and updating relationships
between entities, abstracting direct database interactions.

Classes:
    SQLAlchemyFacadeRelationManager: Manages SQLAlchemy-based operations
    between User, Place, Amenity, and Review, ensuring data consistency.

Dependencies:
    - SQLAlchemy ORM for database interactions.
    - Facades for User, Place, Amenity, and Review, passed as dependencies
      to enable modular and reusable operations on these entities.
"""

from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User


class SQLAlchemyFacadeRelationManager:
    """
    A manager for handling SQLAlchemy-based operations between `User`, `Place`,
    `Amenity` and `Review` entities. This class allows managing relationships
    and associated data modifications in the database.

    Attributes:
        user_facade (UserFacade): Facade for user-related operations.
        place_facade (PlaceFacade): Facade for place-related operations.
        amenity_facade (AmenityFacade): Facade for amenity-related operations.
        review_facade (ReviewFacade): Facade for review-related operations.
    """

    def __init__(self, user_facade, place_facade, amenity_facade, review_facade):
        """
        Initialize SQLAlchemyFacadeRelationManager with the provided facades.

        Args:
            user_facade (UserFacade): Facade for user operations.
            place_facade (PlaceFacade): Facade for place operations.
            amenity_facade (AmenityFacade): Facade for amenity operations.
            review_facade (ReviewFacade): Facade for review operations.
        """
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade

# User - place relations
# <------------------------------------------------------------------------>

    def create_place_for_user(self, user_id, place_data):
        """
        Create a place associated with a specific user.

        Args:
            user_id (str): ID of the user who owns the place.
            place_data (dict): Data for creating the place.

        Returns:
            dict: Dictionary representation of the created place.

        Raises:
            ValueError: If the user is not found.
        """
        print("Using SQLAlchemyFacadeRelationManager "
              "to create place for user")

        user = self.user_facade.user_repo.get(user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        place_data['owner_id'] = user_id
        place_data['owner_first_name'] = user.first_name

        place = self.place_facade.create_place(place_data)
        place_id = place['id']

        if user.places is None:
            user.places = []

        if place_id not in user.places:
            user.places = user.places + [place_id]

        print(f"user.places before commit: {user.places}")
        db.session.add(user)
        db.session.commit()
        print(f"user.places after commit: {user.places}")

        return place

#       <---------------------------------------------------------->

    def delete_place_from_owner_place_list(self, place_id, user_id):
        """
        Delete a place from the owner's list and database.

        Args:
            place_id (str): ID of the place to delete.
            user_id (str): ID of the user owner.

        Raises:
            ValueError: If the user or place is not found \
                in the user's place list.
        """
        print("Using SQLAlchemyFacadeRelationManager "
              "to delete place for user")

        try:
            user = self.user_facade.user_repo.get(user_id)

            if not user:
                raise ValueError(f"User with id: {user_id} not found")

            if place_id in user.places:
                user.places = [pid for pid in user.places if pid != place_id]

                db.session.add(user)
                db.session.commit()

            else:
                raise ValueError(f"Place ID {place_id} not found in user's places list.")

            self.place_facade.place_repo.delete(place_id)

        except ValueError as e:
            print(str(e))

#       <---------------------------------------------------------->

    def delete_user_and_associated_instances(self, user_id):
        """
        Delete a user along with all associated places and related reviews.

        Args:
            user_id (str): ID of the user to delete.

        Raises:
            ValueError: If the user or associated places are not found.
        """
        try:
            user = self.user_facade.user_repo.get(user_id)

            if not user:
                raise ValueError(f"User with id: {user_id} not found")

            places_ids_list = user.places

            if places_ids_list:
                for place_id in places_ids_list:
                    self.delete_place_and_associated_instances(place_id)
            
            self.user_facade.user_repo.delete(user_id)

        except ValueError as e:
            print(f"Une erreur est survenue : {str(e)}")
            raise


        # <------------------------------------------>

    def delete_place_and_associated_instances(self, place_id):
        """
        Delete a place along with all associated reviews.

        Args:
            place_id (str): ID of the place to delete.

        Raises:
            ValueError: If the place or associated reviews are not found.
        """
        try:
            place = self.place_facade.place_repo.get(place_id)

            if not place:
                raise ValueError(f"User with id: {place_id} not found")

            user_id = place.owner_id
            user = self.user_facade.user_repo.get(user_id)

            if not user:
                raise ValueError(f"User with id: {user_id} not found")

            if place_id in user.places:
                user.places = [pid for pid in user.places if pid != place_id]

                db.session.add(user)
                db.session.commit()

            else:
                raise ValueError(
                    f"Place ID {place_id} not found in user's places list.")

            reviews_ids_list = place.reviews

            if reviews_ids_list:
                for review_id in reviews_ids_list:
                    self.review_facade.review_repo.delete(review_id)
            
            self.place_facade.place_repo.delete(place_id)

        except ValueError as e:
            print(f"Une erreur est survenue : {str(e)}")
            raise


#  Place - Amenity relations
# <------------------------------------------------------------------------>

    def add_amenity_to_a_place(self, place_id, amenity_data):
        """
        Add an amenity to a place.

        Args:
            place_id (str): ID of the place to add the amenity.
            amenity_data (dict): Data for creating the amenity.

        Returns:
            dict: Dictionary representation of the added or existing amenity.

        Raises:
            ValueError: If the place or amenity already exists.
        """
        place = self.place_facade.place_repo.get(place_id)

        amenity_name = amenity_data["name"]

        amenity = self.amenity_facade.amenity_repo.get_by_attribute("name", amenity_name)

        if not place:
            raise ValueError(f"Place: {place_id} not found.")

        if not amenity_data["name"] in place.amenities:
            place.amenities = place.amenities + [amenity_data["name"]]

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
        """
        Delete an amenity from a place's amenities list.

        Args:
            amenity_name (str): Name of the amenity to delete.
            place_id (str): ID of the place.

        Raises:
            ValueError: If the place or amenity is not found.
        """
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")

        if amenity_name in place.amenities:
            place.amenities = [amty_name for amty_name in place.amenities if amty_name != amenity_name]

            db.session.add(place)
            db.session.commit()

        else:
            raise ValueError(f"Amenity {amenity_name} not found in places_amenities list.")


# #  Place - review relations
# # <------------------------------------------------------------------------>

    def create_review_for_place(self, place_id, user_id, review_data):
        """
        Create a review for a specific place and associate it with a user.

        Args:
            place_id (str): ID of the place.
            user_id (str): ID of the user creating the review.
            review_data (dict): Data for creating the review.

        Returns:
            dict: Dictionary representation of the created review.

        Raises:
            ValueError: If the place or user is not found.
        """
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

        db.session.add(place)
        db.session.commit()

        return review

        # <------------------------------------------>

    def delete_review_from_place_list(self, review_id, place_id):
        """
        Delete a review from a place's reviews list.

        Args:
            review_id (str): ID of the review to delete.
            place_id (str): ID of the place.

        Raises:
            ValueError: If the place or review is not found.
        """
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")

        reviews = place.reviews

        if review_id in reviews:
            place.reviews = [rev_id for rev_id in reviews if rev_id != review_id]

            db.session.add(place)
            db.session.commit()

        else:
            raise ValueError(f"Review with id: {review_id} not found")

        self.review_facade.review_repo.delete(review_id)
