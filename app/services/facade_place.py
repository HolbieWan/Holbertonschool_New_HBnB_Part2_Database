"""
PlaceFacade provides high-level operations for creating, retrieving,
updating, and deleting places. This service layer interacts with the
place repository.
"""

from app.models.place import Place


class PlaceFacade():
    """
    Service class for managing place operations, including creation, retrieval,
    updating, and deletion of places.
    """

    def __init__(self, selected_repo):
        """
        Initializes the PlaceFacade with a repository.

        Args:
            selected_repo: The repository instance to manage place persistence.
        """
        self.place_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_place(self, place_data):
        """
        Creates a new place.

        Args:
            place_data (dict): Dictionary containing place information
                               including 'title', 'description', 'price',
                               'latitude', 'longitude', 'owner_first_name',
                               and 'owner_id'.

        Returns:
            dict: The created place in dictionary form.

        Raises:
            ValueError: If a place with the same title exists
            or validation fails.
        """
        print(f"Creating place with data: {place_data}")

        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_first_name=place_data["owner_first_name"],
            owner_id=place_data["owner_id"],
            amenities=place_data.get("amenities"),
            reviews=place_data.get("reviews")
        )

        existing_place = self.place_repo.get_by_attribute("title", place.title)

        if existing_place:
            raise ValueError(f"Place '{place.title}' already exists. Please choose another title.")

        if place.is_valid():
            print(f"User {place.title} passed validation.")
            self.place_repo.add(place)

            return place.to_dict()
        
        else:
            print(f"Place: {place.title} failed validation.")
            raise ValueError("Invalid place data.")

    #   <------------------------------------------------------------------------>

    def get_place(self, place_id):
        """
        Retrieves a place by ID.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            dict: The place data in dictionary form.

        Raises:
            ValueError: If the place is not found.
        """
        place = self.place_repo.get(place_id)

        if place:
            return place.to_dict()
        
        else:
            raise ValueError(f"Place with id {place_id} not found.")

    #   <------------------------------------------------------------------------>

    def get_place_by_attribute(self, attr):
        pass

    #   <------------------------------------------------------------------------>

    def get_all_places(self):
        """
        Retrieves all places.

        Returns:
            list: A list of all places in dictionary form.
        """
        places = self.place_repo.get_all()

        return [place.to_dict() for place in places]

    #   <------------------------------------------------------------------------>

    def update_place(self, place_id, new_data):
        """
        Updates a place's data.

        Args:
            place_id (str): The unique identifier of the place to update.
            new_data (dict): Dictionary with the updated place information.

        Returns:
            dict: The updated place data in dictionary form.

        Raises:
            ValueError: If the place is not found.
        """
        place = self.place_repo.get(place_id)

        if not place:
            raise ValueError(f"Place with id {place_id} not found.")
        
        new_place_title = new_data["title"]
        
        existing_place_title = self.place_repo.get_by_attribute("title", new_place_title)

        if existing_place_title and new_place_title != place.title:
            raise ValueError(f"Place with title: {new_place_title} already exists, choose another one.")

        new_place = Place(
            title=new_data["title"],
            description=new_data["description"],
            price=new_data["price"],
            latitude=new_data["latitude"],
            longitude=new_data["longitude"],
            owner_first_name=place.owner_first_name,
            owner_id=place.owner_id,
            amenities=place.amenities,
            reviews=place.reviews
        )

        if not new_place.is_valid():
            raise ValueError("Place validation failed. Please check the email and other attributes.")

        if place:
            self.place_repo.update(place_id, new_data)

            return place.to_dict()
        else:
            raise ValueError(f"place with id {place_id} not found.")

    #   <------------------------------------------------------------------------>

    def delete_place(self, place_id):
        """
        Deletes a place by ID.

        Args:
            place_id (str): The unique identifier of the place to delete.

        Raises:
            ValueError: If the place is not found.
        """
        place = self.place_repo.get(place_id)

        if place:
            print(f"Deleted place: {place}")
            self.place_repo.delete(place_id)
        else:
            raise ValueError(f"Place with id: {place_id} not found !")

    #   <------------------------------------------------------------------------>

    def get_all_places_from_owner_id(self, owner_id):
        """
        Retrieves all places for a specific owner by their ID.

        Args:
            owner_id (str): The owner's unique identifier.

        Returns:
            list: A list of places for the specified owner in dictionary form.

        Raises:
            ValueError: If no places are found for the owner ID.
        """
        places = self.place_repo.get_by_attribute("owner_id", owner_id)

        if places:
            return [place.to_dict() for place in places]
        
        else:
            raise ValueError(f"No place found for owner_id: {owner_id}")
