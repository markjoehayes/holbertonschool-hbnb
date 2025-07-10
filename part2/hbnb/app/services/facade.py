from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new User"""
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
        from models.amenity import Amenity
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

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
