from app.models.place import Place

class PlaceFacade():

    def __init__(self, selected_repo):
        self.place_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_place(self, place_data):
        print(f"Creating place with data: {place_data}")

        place = Place(
            title = place_data["title"],
            description = place_data["description"],
            price = place_data["price"],
            latitude = place_data["latitude"],
            longitude = place_data["longitude"],
            owner_first_name= place_data["owner_first_name"],
            owner_id = place_data["owner_id"],
            amenities=place_data.get("amenities"),
            reviews=place_data.get("reviews") 
        )

        existing_place = self.place_repo.get_by_attribute("title", place.title)
        if existing_place:
            print(f"Place: {place.title} already exists. Please choose another title for your place")
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
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    #   <------------------------------------------------------------------------>

    def update_place(self, place_id, new_data):
        place = self.place_repo.get(place_id)
        if place:
            self.place_repo.update(place_id, new_data)
            return place.to_dict()
        else:
            raise ValueError(f"place with id {place_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            print(f"Deleted place: {place}")
            self.place_repo.delete(place_id)
        else:
            raise ValueError(f"Place with id: {place_id} not found !")
        
    #   <------------------------------------------------------------------------>

    def get_all_places_from_owner_id(self, owner_id):
        places = self.place_repo.get_by_attribute("owner_id", owner_id)
        if places:
            return [place.to_dict() for place in places]
        else:
            raise ValueError(f"No place found for owner_id: {owner_id}")
