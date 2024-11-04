from app.persistence.repo_selector import RepoSelector
from app.models.amenity import Amenity

class AmenityFacade():

    def __init__(self, selected_repo):
        self.amenity_repo = selected_repo

 # <------------------------------------------------------------------------>

    def create_amenity(self, amenity_data):
        print(f"Creating amenity with data: {amenity_data}")

        amenity = Amenity(
            name = amenity_data["name"]
        )

        existing_amenity = self.amenity_repo.get_by_attribute("name", amenity.name)
        if existing_amenity:
            print(f"Amenity: {amenity.name} already exists in amenity repo. Please choose another name for your amenity")
            raise ValueError(f"Amenity '{amenity.name}' already exists. Please choose another name.")

        if amenity.is_valid():
            print(f"Amenity {amenity.name} passed validation.")
            self.amenity_repo.add(amenity)
            print(f"Amenity: {amenity.name} has been added to amenity_repo")
            return amenity.to_dict()
        else:
            print(f"Amenity: {amenity.name} failed validation.")
            raise ValueError("Invalid amenity data.")
        
    #   <------------------------------------------------------------------------>

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict()
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def get_amenity_by_attribute(self, attr):
        pass

    #   <------------------------------------------------------------------------>

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    #   <------------------------------------------------------------------------>

    def update_amenity(self, amenity_id, new_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            self.amenity_repo.update(amenity_id, new_data)
            return amenity.to_dict()
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity_id)
        else:
            raise ValueError(f"Amenity with id: {amenity_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def get_all_amenitys_from_place_id(self, place_id):
        amenities = self.amenity_repo.get_by_attribute("id", place_id)
        if amenities:
            return [amenity.to_dict() for amenity in amenities]
        else:
            raise ValueError(f"No amenity found for place_id: {place_id}")
