from app.persistence.repository import InMemoryRepository
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_atttribute('email', email)

    def get_place(self, place_id):
        # Logic will ve inplemented in later tasks
        pass
    
    def create_amenity(self, amenity_data):
        """Creates a new amenity with validation"""
        try:
            if not amenity_data or 'name' not in amenity_data:
                raise ValueError("Amenity name is required")

            name = amenity_data.get('name', '').strip()
            if not name:
                raise ValueError("Amenity name cannot be empty")
            
            # check if amenity with same name already exists
            existing_amenities = self.get_all_amenities()
            for amenity in existing_amenities:
                if amenity.name.lower() == name.lower():
                    raise ValueError(f"Amenity with name '{name}' already exists")

            # create a new amenity instance
            new_amenity = Amenity(name=name)

            # save to a repository
            created_amenity = self.amenity_repo.create(new_amenity)
            return created_amenity

        except Exception as e:
            # log the error and re-raise
            print(f"Error creating amenity: {e}")
            raise Exception("Failed to create amenity")

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        try:
            if not amenity_id:
                raise ValueError("Amenity ID is required")

            amenity = self.amenity_repo.get_by_id(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")

            return amenity

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error retrieving amenity {amenity_id}: {e}")
            raise Exception("Failed to retrieve amenity")

    def get_all_amenities(self):
        """Retrieve all amenities"""
        try:
            amenities = self.amenity_repo.get_all()
            return amenities or []

        except Exception as e:
            print(f"Error retrieving all amenities: {e}")
            raise Exception("Failed to retrieve amenities")

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity"""
        try:
            if not amenity_id:
                raise ValueError("Amenity ID is required")

            if not amenity_data:
                raise ValueError("Update data is required")

            # Check if amenity exists
            existing_amenity = self.get_amenity(amenity_id)
            if not existing_amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")

            # Validate name if provided
            if 'name' in amenity_data:
                name = amenity_data.get('name', '').strip()
                if not name:
                    raise ValueError("Amenity name cannot be empty")

                # Check for duplicate names (excluding current amenity)
                existing_amenities = self.get_all_amenities()
                for amenity in existing_amenities:
                    if (amenity.id != amenity_id and
                        amenity.name.lower() == name.lower()):
                        raise ValueError(f"Amenity with name '{name}' already exists")

            # Update amenity - your model's __init__ validation will handle the 50 char limit
            # Need to create a new Amenity instance to trigger the validation
            if 'name' in amenity_data:
                       # This will raise ValueError if name exceeds 50 chars (from your _validate_name)
                test_amenity = Amenity(name=amenity_data['name'])

            # Prepare update data
            update_data = {}
            if 'name' in amenity_data:
                update_data['name'] = amenity_data['name'].strip()

            # Update amenity
            updated_amenity = self.amenity_repo.update(amenity_id, update_data)
            return updated_amenity

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error updating amenity {amenity_id}: {e}")
            raise Exception("Failed to update amenity")

    def create_place(self, place_data):
        """Create a new place with validation"""
        try:
            # Validate required fields
            required_fields = ['title', 'price', 'owner_id']
            for field in required_fields:
                if field not in place_data:
                    raise ValueError(f"{field} is required")

            # Create new place - this will trigger validation in the Place class
            new_place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data.get('latitude', 0.0),
                longitude=place_data.get('longitude', 0.0),
                owner_id=place_data['owner_id']
            )

            # Handle amenities if provided
            if 'amenities' in place_data:
                for amenity_id in place_data['amenities']:
                    pass

            # Save to repository
            self.place_repo.add(new_place)
            return new_place

        except ValueError as e:
            # Re-raise validation errors from Place class
            raise e
        except Exception as e:
            print(f"Error creating place: {e}")
            raise Exception("Failed to create place")

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        try:
            if not place_id:
                raise ValueError("Place ID is required")

            place = self.place_repo.get(place_id)
            if not place:
                raise ValueError(f"Place with ID {place_id} not found")

            return place

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error retrieving place {place_id}: {e}")
            raise Exception("Failed to retrieve place")

    def get_all_places(self):
        """Retrieve all Places"""
        try:
            places = self.place_repo.get_all()
            return places or []

        except Exception as e:
            print(f"Error retrieving all places: {e}")
            raise Exception("Failed to retrieve places")

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        try:
            if not place_id:
                raise ValueError("Place ID is required")

            if not place_data:
                raise ValueError("Update data is required")

            # Check if place exists
            existing_place = self.get_place(place_id)
            if not existing_place:
                raise ValueError(f"Place with ID {place_id} not found")

            # Validate and update fields
            updatable_fields = ['title', 'description', 'price', 'latitude', 'longitude']

            for field in updatable_fields:
                if field in place_data:
                    # Use property setters for validation (for price, latitude, longitude)
                    setattr(existing_place, field, place_data[field])

            return existing_place

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error updating place {place_id}: {e}")
            raise Exception("Failed to update place")
