from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review class that inherits from BaseModel"""

    __tablename__ = "reviews"

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Define relationships 
    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def __init__(self, text="", rating=0, user=None, user_id="", place=None, place_id=""):
        """Initializes Review with defaults"""
        super().__init__()
        self.text = text
        self.rating = self.validate_rating(rating)
        self.user_id = user.id if user else user_id
        self.place_id = place.id if place else place_id

    def validate_rating(self, rating):
        """Ensure rating is between 1 and 5"""
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def __repr__(self):
        return f"<Review {self.id} {self.rating}★>"
