"""
Amenity model providing an entity representing amenities for places.
"""

from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """
    Amenity model that defines an amenity with a unique name.

    Attributes:
        name (str): The name of the amenity.
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """
        Initialize an Amenity instance.

        Args:
            name (str): Name of the amenity.
        """
        super().__init__()
        self.name = name

    def is_valid(self):
        """
        Validate the Amenity instance to ensure data integrity.

        Returns:
            bool: True if amenity data is valid, False otherwise.

        Raises:
            TypeError: If 'name' is not a string.
            ValueError: If 'name' is empty or exceeds 50 characters.
        """
        try:
            if not isinstance(self.name, str):
                raise TypeError("name must be strings (str).")

            stripped_name = self.name.strip()

            if len(stripped_name) == 0 or len(stripped_name) > 50:
                raise ValueError(
                    "Name must not be empty and less than 50 characters.")

            return True

        except TypeError as te:
            print(f"Type error: {str(te)}")
            return False

        except ValueError as ve:
            print(f"Value error: {str(ve)}")
            return False

    def to_dict(self):
        """
        Convert the Amenity instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the amenity.
        """
        return {
            "type": "amenity",
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
