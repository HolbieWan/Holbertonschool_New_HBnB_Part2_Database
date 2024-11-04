from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, place_name, user_id, user_first_name):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.place_name = place_name
        self.user_id = user_id
        self.user_first_name = user_first_name

    def is_valid(self):
        try:
            if not isinstance(self.text, str):
                raise TypeError("text must be strings (str).")
            
            if not isinstance(self.rating, int):
                raise TypeError("rating must be an integer (int).")
            
            if self.rating < 1 or self.rating > 5:
                raise ValueError("rating must be between 1 and 5.")
            
            if self.text == "" or self.place_name == "" or self.place_id == "" or self.user_id == "" or self.user_first_name=="":
                raise ValueError("Fields can not be empty !")
            
            return True

        except TypeError as te:
            print(f"Type error: {str(te)}")
            return False

        except ValueError as ve:
            print(f"Value error: {str(ve)}")
            return False

    def to_dict(self):
        return {
            "type" : "review",
            "id" : self.id,
            "text" : self.text,
            "rating" : self.rating,
            "place_id" : self.place_id,
            "place_name" : self.place_name,
            "user_id" : self.user_id,
            "user_first_name" : self.user_first_name,
            "created_at" : self.created_at.isoformat(),
            "updated_at" : self.updated_at.isoformat()
        }
