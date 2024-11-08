"""
Facade class for the HBnB application,
providing access to various service facades.
"""


class HBnBFacade:
    """
    The HBnBFacade class aggregates different service facades for user, place,
    amenity, and review operations,
    allowing to have a separate facade for each component .
    """

    def __init__(self, user_facade, place_facade, amenity_facade, review_facade):
        """
        Initializes the HBnBFacade with specific service facades.

        Args:
            user_facade: Facade handling user-related operations.
            place_facade: Facade managing place-related operations.
            amenity_facade: Facade handling amenity-related operations.
            review_facade: Facade managing review-related operations.
        """
        self.user_facade = user_facade
        self.place_facade = place_facade
        self.amenity_facade = amenity_facade
        self.review_facade = review_facade
