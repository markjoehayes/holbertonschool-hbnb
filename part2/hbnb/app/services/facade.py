from app.persistence.repository import InMemoryRepository

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
            # We need to create a new Amenity instance to trigger the validation
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
