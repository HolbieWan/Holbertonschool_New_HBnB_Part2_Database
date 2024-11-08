"""
Review model representing user reviews for places.
"""
from app.models.base_model import BaseModel
from app.extensions import db


class Review(BaseModel):
    """
    Review model to define user reviews for places,
    including ratings and comments.

    Attributes:
        text (str): The review content.
        rating (int): The rating score from 1 to 5.
        place_id (str): The identifier of the reviewed place.
        place_name (str): The name of the reviewed place.
        user_id (str): The identifier of the user who created the review.
        user_first_name (str): The first name of the user who created the
        review.
    """
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(), nullable=False)
    place_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    user_first_name = db.Column(db.String(50), nullable=False)

    def __init__(self, text, rating, place_id, place_name, user_id, user_first_name):
        """
        Initialize a Review instance.

        Args:
            text (str): Content of the review.
            rating (int): Rating from 1 to 5.
            place_id (str): ID of the reviewed place.
            place_name (str): Name of the reviewed place.
            user_id (str): ID of the user creating the review.
            user_first_name (str): First name of the reviewing user.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.place_name = place_name
        self.user_id = user_id
        self.user_first_name = user_first_name

    def is_valid(self):
        """
        Validate the Review instance to ensure data integrity.

        Returns:
            bool: True if review data is valid, False otherwise.

        Raises:
            TypeError: If 'text' is not a string or 'rating' is not an integer
            ValueError: If 'rating' is not between 1 and 5,
                        or if any fields are empty.
        """
        try:
            if not all(isinstance(attr, str) for attr in [self.text, self.place_id, self.place_name, self.user_id, self.user_first_name]):
                raise TypeError("text, place_id, place_name, user_id, user_first_name must be strings.")

            if not isinstance(self.rating, int):
                raise TypeError("rating must be an integer (int).")

            if self.rating < 1 or self.rating > 5:
                raise ValueError("rating must be between 1 and 5.")

            if not (0 < len(self.text) <= 50):
                raise ValueError("text must not be empty and should be less than 50 characters.")
            
            if not (0 < len(self.place_name) <= 50):
                raise ValueError("place_name must not be empty and should be less than 50 characters.")
            
            if not (0 < len(self.place_id) <= 50):
                raise ValueError("place_id must not be empty and should be less than 50 characters.")
            
            if not (0 < len(self.user_id) <= 50):
                raise ValueError("user_id must not be empty and should be less than 50 characters.")
            
            if not (0 < len(self.user_first_name) <= 50):
                raise ValueError("user_first_name must not be empty and should be less than 50 characters.")

        except TypeError as te:
            raise ValueError(f"{str(te)}")
        
        except ValueError as ve:
            raise ValueError(f"{str(ve)}")
        
        return True

    def to_dict(self):
        """
        Convert the Review instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the review.
        """
        return {
            "type": "review",
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "place_name": self.place_name,
            "user_id": self.user_id,
            "user_first_name": self.user_first_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
