from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new User"""
        from app.models.user import User
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a single user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.list()

    def update_user(self, user_id, update_data):
        """Update a user's information"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        #Don't allow updating email if already taken by another user
        if 'email' in update_data:
            existing_user = self.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        user.update(update_data)
        return user

    def create_amenity(self, amenity_data):
        """Creates a new amenity"""
        from app.models.amenity import Amenity
        if not amenity_data or 'name' not in amenity_data:
            raise ValueError('Amenity name is required')

        new_amenity = Amenity(**amenity_data)
        self._repo.save(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by ID"""
        amenity = self._repo.get(Amenity, amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
        return amenity

    def get_all_amenities(self):
        """Retrieves all amenities"""
        return self._repo.all(Amenity)

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing amenity"""
        amenity = self.get_amenity(amenity_id)
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        self._repo.save(amenity)
        return amenity

    def create_place(self, place_data):
        """Create a new place with validation"""
        from app.models.place import Place
        from models.user import User
    
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        if not all(field in place_data for field in required_fields):
            raise ValidationError("Missing required fields")
    
        # Validate owner exists
        owner = self._repo.get(User, place_data['owner_id'])
        if not owner:
            raise NotFoundError("Owner not found")
    
        # Create and save place
        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id'],
            amenities=place_data.get('amenities', [])
        )
        self._repo.save(new_place)
        return new_place

    def get_place(self, place_id):
        """Get place by ID with relationships"""
        from models.place import Place
        place = self._repo.get(Place, place_id)
        if not place:
            raise NotFoundError("Place not found")
        return place

    def get_all_places(self):
        """Get all places with basic info"""
        from models.place import Place
        return self._repo.all(Place)

    def update_place(self, place_id, place_data):
        """Update existing place"""
        place = self.get_place(place_id)
    
        # Validate and update fields
        for field, value in place_data.items():
            if hasattr(place, field):
                setattr(place, field, value)
    
        self._repo.save(place)
        return place

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
