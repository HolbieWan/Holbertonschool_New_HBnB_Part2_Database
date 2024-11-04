

class HBnBFacade:
    def __init__(self, user_facade, place_facade, amenity_facade, review_facade):
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade
