# place.py
from app.models.base_model import BaseModel
from app.extensions import db


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_first_name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.Column(db.JSON, default=[])
    amenities = db.Column(db.JSON, default=[])


    def __init__(self, title, description, price, latitude, longitude, owner_id, owner_first_name, amenities=None, reviews=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_first_name = owner_first_name
        self.owner_id = owner_id
        self.reviews = reviews if reviews is not None else []
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to a place."""
        self.amenities.append(amenity)

    def is_valid(self):
        try:
            if not all(isinstance(attr, str) for attr in [self.title, self.description]):
                raise TypeError("title and description must be strings (str).")
            
            if self.price < 0:
                raise ValueError("price must be a positiv value")
            
            if len(self.title) > 100:
                raise ValueError("title must be less than 100 characters.")
            
            if not all(isinstance(attr, float) for attr in [self.price, self.latitude, self.longitude]):
                raise TypeError("price, latitude, and longitude must be floats (float).")

            if self.latitude > 90 or self.latitude < -90:
                raise ValueError("Must be within the range of -90.0 to 90.0")
            
            if self.longitude > 180 or self.latitude < -180:
                raise ValueError("Must be within the range of -90.0 to 90.0")
            
            return True

        except TypeError as te:
            print(f"Type error: {str(te)}")
            return False

        except ValueError as ve:
            print(f"Value error: {str(ve)}")
            return False

    def to_dict(self):
        return {
            "type": "place",
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "price" : self.price,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "owner_first_name" : self.owner_first_name,
            "owner_id" : self.owner_id,
            "reviews" : self.reviews,
            "amenities" : self.amenities,
            "created_at" : self.created_at.isoformat(),
            "updated_at" : self.updated_at.isoformat()
        }
