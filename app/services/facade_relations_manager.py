"""
FacadeRelationManager handles complex operations that involve relationships
between users, places, amenities, and reviews. It leverages individual facades
and repositories to manage entity interconnections.
"""

from app.persistence.repository import SQLAlchemyRepository


class FacadeRelationManager:
    """
    Manages interactions between users, places, amenities, and reviews,
    including creation, deletion, and relationship management.
    """

    def __init__(

            self,
            user_facade,
            place_facade,
            amenity_facade,
            review_facade):
        """
        Initialize the FacadeRelationManager with specific entity facades.

        Args:
            user_facade: Facade for user operations.
            place_facade: Facade for place operations.
            amenity_facade: Facade for amenity operations.
            review_facade: Facade for review operations.
        """
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade

# User - place relations
# <------------------------------------------------------------------------>

    def create_place_for_user(self, user_id, place_data):
        """
        Creates a new place associated with a user.

        Args:
            user_id (str): ID of the user creating the place.
            place_data (dict): Data for the new place.

        Returns:
            dict: Created place information.

        Raises:
            ValueError: If the user is not found.
        """
        print("Using FacadeRelationManager to create place for user")

        user = self.user_facade.user_repo.get(user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        place_data['owner_id'] = user_id
        place_data['amenities'] = []
        place_data['reviews'] = []
        place_data['owner_first_name'] = user.first_name

        place = self.place_facade.create_place(place_data)

        if isinstance(self.user_facade.user_repo, SQLAlchemyRepository):
            user.places.append(place)
        else:
            user.places.append(place['id'])

        self.user_facade.user_repo.update(user_id, user.to_dict())

        return place

        # <------------------------------------------>

    def delete_place_from_owner_place_list(self, place_id, user_id):
        """
        Removes a place from a user's place list and deletes it.

        Args:
            place_id (str): ID of the place to be removed.
            user_id (str): ID of the user who owns the place.

        Raises:
            ValueError: If the user or place is not found.
        """
        user = self.user_facade.user_repo.get(user_id)

        if not user:
            raise ValueError(f"User with id: {user_id} not found")

        places = user.places

        if place_id in places:
            places.remove(place_id)
            self.user_facade.user_repo.update(user_id, user.to_dict())

        else:
            raise ValueError(
                f"Place ID {place_id} not found in user's places list.")

        self.place_facade.place_repo.delete(place_id)

        # <------------------------------------------>

    def delete_user_and_associated_instances(self, user_id):
        """
        Deletes a user and their associated places.

        Args:
            user_id (str): ID of the user to delete.

        Raises:
            ValueError: If the user or any associated place is not found.
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
        Deletes a place and its associated reviews.

        Args:
            place_id (str): ID of the place to delete.

        Raises:
            ValueError: If the place or its associated user is not found.
        """
        try:
            place = self.place_facade.place_repo.get(place_id)

            if not place:
                raise ValueError(f"Place with id: {place_id} not found")
            
            user_id = place.owner_id

            user = self.user_facade.user_repo.get(user_id)

            if not user:
                raise ValueError(f"User with id: {user_id} not found")

            user_places = user.places

            if place_id in user_places:
                user_places.remove(place_id)
                self.user_facade.user_repo.update(user_id, user.to_dict())

            else:
                raise ValueError(f"Place ID {place_id} not found in user's places list.")

            reviews_ids_list = place.reviews

            if reviews_ids_list:
                for review_id in reviews_ids_list:
                    self.review_facade.review_repo.delete(review_id)

            else:
                raise ValueError(f"No corresponding review found for this place.")
            
            self.place_facade.place_repo.delete(place_id)
            print(f"Place with id: {place_id} has been successfully deleted")

        except ValueError as e:
            print(f"Une erreur est survenue : {str(e)}")
            raise
 

#  Place - Amenity relations
# <------------------------------------------------------------------------>

    def add_amenity_to_a_place(self, place_id, amenity_data):
        """
        Adds an amenity to a place.

        Args:
            place_id (str): ID of the place.
            amenity_data (dict): Data of the amenity to add.

        Returns:
            dict: The added amenity information.

        Raises:
            ValueError: If the place or amenity already exists.
        """
        place = self.place_facade.place_repo.get(place_id)
        amenity_name = amenity_data["name"]
        existing_amenity = self.amenity_facade.amenity_repo.get_by_attribute("name", amenity_name)

        if not place:
            raise ValueError(f"Place: {place_id} not found.")
        
        if amenity_name in place.amenities:
            raise ValueError(f"Amenity: {amenity_data['name']} already exist for this place: {place_id}")

        if not ( 0 < len(amenity_name) < 50):
            raise ValueError(f"name must not be empty and less than 50 characters")
        
        else:
            place.amenities.append(amenity_name)
            self.place_facade.place_repo.update(place_id, place.to_dict())
            print(f"Amenity: {amenity_name} has been added to the place: {place_id}")

            if not existing_amenity:
                amenity = self.amenity_facade.create_amenity(amenity_data)

        return amenity

        # <------------------------------------------>

    def get_all_amenities_id_from_place(self, place_id):
        """
        Removes an amenity from a place.

        Args:
            amenity_name (str): Name of the amenity.
            place_id (str): ID of the place.

        Raises:
            ValueError: If the place or amenity is not found.
        """
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place: {place_id} not found")

        amenities = place.amenities

        if not amenities:
            raise ValueError(f"No amenities found for the place: {place_id}")

        return amenities

        # <------------------------------------------>

    def get_all_amenities_names_from_place(self, place_id):
        """
        Retrieves all places with a specified amenity.

        Args:
            amenity_name (str): Name of the amenity.

        Returns:
            list: List of places that have the specified amenity.

        Raises:
            ValueError: If no places with the amenity are found.
        """
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place: {place_id} not found")

        amenities = place.amenities

        if not amenities:
            raise ValueError(f"No amenities found for this place: {place_id}")

        return amenities

        # <------------------------------------------>

    def delete_amenity_from_place_list(self, amenity_name, place_id):
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")

        amenities = place.amenities

        if amenity_name in amenities:
            amenities.remove(amenity_name)
            self.place_facade.place_repo.update(place_id, place.to_dict())

        else:
            raise ValueError(f"Amenity {amenity_name} not found in places_amenities list.")

        self.amenity_facade.amenity_repo.delete(amenity_name)

        # <------------------------------------------>

    def get_all_places_with_specifique_amenity(self, amenity_name):
        """
        Retrieves all places with a specified amenity.

        Args:
            amenity_name (str): Name of the amenity.

        Returns:
            list: List of places that have the specified amenity.

        Raises:
            ValueError: If no places with the amenity are found.
        """
        places = self.place_facade.get_all_places()

        if not places:
            raise ValueError("No place found in place_repo")

        place_amenity_name_list = []

        for place in places:
            if amenity_name in place["amenities"]:
                place_amenity_name_list.append(place)

        if not place_amenity_name_list:
            raise ValueError(f"No place found with the amenity: {amenity_name}")

        return place_amenity_name_list


# #  Place - review relations
# # <------------------------------------------------------------------------>

    def create_review_for_place(self, place_id, user_id, review_data):
        """
        Creates a review for a place.

        Args:
            place_id (str): ID of the place to review.
            user_id (str): ID of the user creating the review.
            review_data (dict): Data of the review.

        Returns:
            dict: The created review information.

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
        place.reviews.append(review['id'])
        self.place_facade.place_repo.update(place_id, place.to_dict())

        return review

#         # <------------------------------------------>

    def get_all_reviews_dict_from_place_reviews_id_list(self, place_id):
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"User with id: {place_id} not found")

        reviews_id_list = place.reviews

        reviews_dict_list = []

        for review_id in reviews_id_list:
            review = self.review_facade.review_repo.get(review_id)
            reviews_dict_list.append(review)

        if not reviews_dict_list:
            raise ValueError(f"No reviews found for this place: {place_id}")

        return reviews_dict_list

#         # <------------------------------------------>

    def get_all_reviews_id_from_place(self, place_id):
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"User with id: {place_id} not found")

        reviews = place.reviews

        return reviews

#         # <------------------------------------------>

    def delete_review_from_place_list(self, review_id, place_id):
        """
        Removes a review from a place.

        Args:
            review_id (str): ID of the review to delete.
            place_id (str): ID of the place associated with the review.

        Raises:
            ValueError: If the place or review is not found.
        """
        place = self.place_facade.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id: {place_id} not found")

        reviews = place.reviews

        if review_id in reviews:
            reviews.remove(review_id)
            self.place_facade.place_repo.update(place_id, place.to_dict())
            
        else:
            raise ValueError(f"Review with id: {review_id} not found")

        self.review_facade.review_repo.delete(review_id)


# #  User - review relations
# # <------------------------------------------------------------------------>

    def get_all_reviews_from_user(self, user_id):
        """
        Retrieves all reviews made by a user.

        Args:
            user_id (str): ID of the user.

        Returns:
            list: List of reviews made by the user.

        Raises:
            ValueError: If the user has no reviews or does not exist.
        """
        user = self.user_facade.user_repo.get(user_id)
        reviews = self.review_facade.review_repo.get_all()

        if not user:
            raise ValueError("This user does not exist")

        if not reviews:
            raise ValueError("No review found in review repo")

        user_reviews_list = []

        for review in reviews:
            if user_id in review.user_id:
                review.type = "review"
                user_reviews_list.append(review)

        if not user_reviews_list:
            raise ValueError(f"No review found for this user: {user_id}")

        return user_reviews_list
