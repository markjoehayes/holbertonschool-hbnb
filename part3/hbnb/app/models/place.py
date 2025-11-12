from app import db
from app.models.base_model import BaseModel

# --- Association table for Place <-> Amenity ---
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Defines the Place class with validation"""

    __tablename__ = "places"

    # ----Columns --------
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255))
    _price = db.Column("price", db.Float, nullable=False, default=0.0)
    _latitude = db.Column("latitude", db.Float, default=0.0)
    _longitude = db.Column("longitude", db.Float, default=0.0)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # --- Relationships ---
    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = db.relationship(
        "Amenity",
        secondary="place_amenities",
        back_populates="places"
    )


    def __init__(self, title="", description="", price=0.0, latitude=0.0, longitude=0.0, owner=None, owner_id=""):
        
        """Initializes the Place Class with validation"""
        super().__init__()
        self.title = title
        self.description = description
        self._price = price
        self._latitude = latitude
        self._longitude = longtitude
        self.owner_id = owner.id if owner else owner_id

    def add_review(self, review):
        """Associate a review with this place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def __repr__(self):
        return f"<Place {self.id}: {self.title}>"

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
