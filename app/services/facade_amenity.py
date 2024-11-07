"""
AmenityFacade provides high-level operations for creating, retrieving,
updating, and deleting amenities. This service layer interacts with the
amenity repository.
"""

from app.models.amenity import Amenity


class AmenityFacade():
    """
    Service class for managing amenity operations, including creation,
    retrieval, updating, and deletion of amenities.
    """

    def __init__(self, selected_repo):
        """
        Initializes the AmenityFacade with a repository.

        Args:
            selected_repo: The repository instance to manage \
                amenity persistence.
        """
        self.amenity_repo = selected_repo

# <------------------------------------------------------------------------>

    def create_amenity(self, amenity_data):
        """
        Creates a new amenity.

        Args:
            amenity_data (dict): Dictionary containing amenity information,
                                 including 'name'.

        Returns:
            dict: The created amenity in dictionary form.

        Raises:
            ValueError: If an amenity with the same name exists \
                or validation fails.
        """
        print(f"Creating amenity with data: {amenity_data}")

        amenity = Amenity(
            name=amenity_data["name"]
        )

        existing_amenity = self.amenity_repo.get_by_attribute(
            "name", amenity.name)

        if existing_amenity:
            print(
                f"Amenity: {amenity.name} already exists in amenity repo. "
                "Please choose another name for your amenity")
            raise ValueError(
                f"Amenity '{amenity.name}' already exists. "
                "Please choose another name.")

        if amenity.is_valid():
            print(f"Amenity {amenity.name} passed validation.")
            self.amenity_repo.add(amenity)
            print(f"Amenity: {amenity.name} has been added to amenity_repo")
            return amenity.to_dict()
        else:
            print(f"Amenity: {amenity.name} failed validation.")
            raise ValueError("Invalid amenity data.")

    #   <-------------------------------------------------------------------->

    def get_amenity(self, amenity_id):
        """
        Retrieves an amenity by ID.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            dict: The amenity data in dictionary form.

        Raises:
            ValueError: If the amenity is not found.
        """
        amenity = self.amenity_repo.get(amenity_id)

        if amenity:
            return amenity.to_dict()
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")

    #   <-------------------------------------------------------------------->

    def get_amenity_by_attribute(self, attr):
        pass

    #   <-------------------------------------------------------------------->

    def get_all_amenities(self):
        """
        Retrieves all amenities.

        Returns:
            list: A list of all amenities in dictionary form.
        """
        amenities = self.amenity_repo.get_all()

        return [amenity.to_dict() for amenity in amenities]

    #   <-------------------------------------------------------------------->

    def update_amenity(self, amenity_id, new_data):
        """
        Updates an amenity's data.

        Args:
            amenity_id (str): The unique identifier of the amenity to update.
            new_data (dict): Dictionary with the updated amenity information.

        Returns:
            dict: The updated amenity data in dictionary form.

        Raises:
            ValueError: If the amenity is not found.
        """
        amenity = self.amenity_repo.get(amenity_id)

        if amenity:
            self.amenity_repo.update(amenity_id, new_data)

            return amenity.to_dict()
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")

    #   <-------------------------------------------------------------------->

    def delete_amenity(self, amenity_id):
        """
        Deletes an amenity by ID.

        Args:
            amenity_id (str): The unique identifier of the amenity to delete.

        Raises:
            ValueError: If the amenity is not found.
        """
        amenity = self.amenity_repo.get(amenity_id)

        if amenity:
            self.amenity_repo.delete(amenity_id)
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")

    #   <-------------------------------------------------------------------->

    def get_all_amenitys_from_place_id(self, place_id):
        """
        Retrieves all amenities associated with a specific place by its ID.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A list of amenities for the specified place \
                in dictionary form.

        Raises:
            ValueError: If no amenities are found for the place ID.
        """
        amenities = self.amenity_repo.get_by_attribute("id", place_id)

        if amenities:
            return [amenity.to_dict() for amenity in amenities]
        else:
            raise ValueError(f"No amenity found for place_id: {place_id}")
