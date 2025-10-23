from app.models.base_model import BaseModel
"""Defines a class for Place"""

class Place(BaseModel):
    """Defines the Place class with validation"""

    def __init__(self, title="", description="", price=0.0, latitude=0.0, longitude=0.0, owner=None, owner_id=""):
        
        """Initializes the Place Class with validation"""
        super().__init__()
        self.title = title
        self.description = description

        #initialize private attributes for properties
        self._price = 0.0
        self._latitude = 0.0
        self._longitude = 0.0

        self.owner_id = owner.id if owner else owner_id
        self.reviews = [] # list to store related reviews
        self.amenities = [] # list to store related amenities

        # Use property setters to trigger validation
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Place ({self.id}) {self.title} - ${self.price}"

      # Price property with validation
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """Validate price is non-negative float"""
        try:
            price_val = float(value)
            if price_val < 0:
                raise ValueError("Price cannot be negative")
            self._price = price_val
        except (TypeError, ValueError):
            raise ValueError("Price must be a valid non-negative number")

     # Latitude property with validation
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Validate latitude between -90 and 90"""
        try:
            lat_val = float(value)
            if not -90 <= lat_val <= 90:
                raise ValueError("Latitude must be between -90 and 90")
            self._latitude = lat_val
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a valid number between -90 and 90")


     # Longitude property with validation  
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Validate longitude between -180 and 180"""
        try:
            long_val = float(value)
            if not -180 <= long_val <= 180:
                raise ValueError("Longitude must be between -180 and 180")
            self._longitude = long_val
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a valid number between -180 and 180")

    def to_dict(self):
        """Return dictionary representation with proper formatting"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'latitude': float(self.latitude), 
            'longitude': float(self.longitude),
            'owner_id': self.owner_id,
            'amenities': [amenity.id for amenity in self.amenities],
            'reviews': [review.id for review in self.reviews]
        })
        return place_dict


    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenities(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)

    #def remove_amenity(self, amenity):
    #    """Remove an amenity from the place"""
    #    if amenity in self.amenities:
    #        self.amenities.remove(amenity)
