from app.models.base_model import BaseModel
from app.models.review import Review

class Review(BaseModel):
    """Review class that inherits from BaseModel"""
    def __init__(self, text="", rating=0, user=None, user_id="", place=None, place_id=""):
        """Initializes Review with defaults"""
        super().__init__()
        self.text = text
        self.rating = self.validate_rating(rating)
        self.user_id = user.id if user else user_id
        self.place_id = place.id if place else place_id

    def validate_rating(self, rating):
        """Ensure rating is between 1 and 5"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def __str__(self):
        return f"Review ({self.id}): {self.text} - {self.rating}*"
