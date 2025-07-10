from .BaseClass import BaseModel  
from .user import User           
from .amenity import Amenity     

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = amenities or []  # List to store related reviews
        self.amenities = amenities if amenities is not None else []  # List to store related amenities

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and must be 100 characters or less")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    @property
    def owner_id(self):
        return self._owneri_id

    @owner_id.setter
    def owner_id(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("Owner must be a non-empty string")
        self._owner_id = value


    def add_amenity(self, amenity_id):
        """Add an amenity to the place."""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity)
