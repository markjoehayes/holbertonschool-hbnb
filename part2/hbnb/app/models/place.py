from app.models.base_model import BaseModel
"""Defines a class for Place"""

class Place(BaseModel):
    """Defines the Place class"""

    def __init__(self, title="", description="", price=0.0, latitude=0.0, longitude=0.0, owner=None, owner_id=""):
        
        """Initializes the Place Class"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id if owner else owner_id
        self.reviews = [] # list to store related reviews
        self.amenities = [] # list to store related amenities

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenities(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)

