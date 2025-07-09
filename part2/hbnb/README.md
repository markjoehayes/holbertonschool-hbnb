# Business Logic Layer Implementation

This project implements the core business logic for a property rental platform with the following entities:

## User
- Represents users of the platform
- Can own places and write reviews
- Attributes: id, first_name, last_name, email, is_admin, created_at, updated_at

## Place
- Represents rental properties
- Can have reviews and amenities
- Attributes: id, title, description, price, latitude, longitude, owner, created_at, updated_at

## Review
- Represents user reviews of places
- Attributes: id, text, rating, place, user, created_at, updated_at

## Amenity
- Represents features available at places
- Attributes: id, name, created_at, updated_at

## API Endpoints Documentation

### User API Endpoints Documentation

#### Create a User
`POST /api/v1/users/`

Request body:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}

## Example Usage

```python
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

# Create a user
owner = User(first_name="John", last_name="Doe", email="john@example.com")

# Create a place
place = Place(
    title="Beach House",
    description="Lovely beachfront property",
    price=200,
    latitude=34.0522,
    longitude=-118.2437,
    owner=owner
)

# Add an amenity
wifi = Amenity(name="Wi-Fi")
place.add_amenity(wifi)

# Add a review
review = Review(
    text="Amazing views!",
    rating=5,
    place=place,
    user=owner
)
