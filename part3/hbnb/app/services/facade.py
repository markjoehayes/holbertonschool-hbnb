from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user"""
        #user = User(**user_data) #change for security reasons
        user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
    
         # Update allowed fields only
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
    
        user.save()
        return user

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

    def create_review(self, review_data):
        """Create a new review with validation"""
        try:
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in review_data:
                    raise ValueError(f"{field} is required")
        
            # Validate user exists
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError(f"User with ID {review_data['user_id']} not found")
        
            # Validate place exists
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError(f"Place with ID {review_data['place_id']} not found")
        
            # Validate text is not empty
            text = review_data['text'].strip()
            if not text:
                raise ValueError("Review text cannot be empty")
        
            # Create new review - this will trigger rating validation
            new_review = Review(
                text=text,
                rating=review_data['rating'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id']
            )
        
            # Save to repository
            self.review_repo.add(new_review)
        
            # Add review to place's reviews list
            place.add_review(new_review)
        
            return new_review
        
        except ValueError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            print(f"Error creating review: {e}")
            raise Exception("Failed to create review")

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        try:
            if not review_id:
                raise ValueError("Review ID is required")
        
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError(f"Review with ID {review_id} not found")
        
            return review
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error retrieving review {review_id}: {e}")
            raise Exception("Failed to retrieve review")

    def get_all_reviews(self):
        """Retrieve all reviews"""
        try:
            reviews = self.review_repo.get_all()
            return reviews or []
        
        except Exception as e:
            print(f"Error retrieving all reviews: {e}")
            raise Exception("Failed to retrieve reviews")

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        try:
            if not place_id:
                raise ValueError("Place ID is required")
        
            # Validate place exists
            place = self.place_repo.get(place_id)
            if not place:
                raise ValueError(f"Place with ID {place_id} not found")
        
            # Get all reviews and filter by place_id
            all_reviews = self.get_all_reviews()
            place_reviews = [review for review in all_reviews if review.place_id == place_id]
        
            return place_reviews
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error retrieving reviews for place {place_id}: {e}")
            raise Exception("Failed to retrieve reviews for place")

    def update_review(self, review_id, review_data):
        """Update a review"""
        try:
            if not review_id:
                raise ValueError("Review ID is required")
        
            if not review_data:
                raise ValueError("Update data is required")
        
            # Check if review exists
            existing_review = self.get_review(review_id)
            if not existing_review:
                raise ValueError(f"Review with ID {review_id} not found")
        
            # Validate and update fields
            updatable_fields = ['text', 'rating']
        
            for field in updatable_fields:
                if field in review_data:
                    if field == 'text':
                        # Validate text is not empty
                        text = review_data['text'].strip()
                        if not text:
                            raise ValueError("Review text cannot be empty")
                        existing_review.text = text
                    elif field == 'rating':
                        # Use the validate_rating method
                        existing_review.rating = existing_review.validate_rating(review_data['rating'])
        
            return existing_review
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error updating review {review_id}: {e}")
            raise Exception("Failed to update review")

    def delete_review(self, review_id):
        """Delete a review"""
        try:
            if not review_id:
                raise ValueError("Review ID is required")
        
            # Check if review exists
            review = self.get_review(review_id)
            if not review:
                raise ValueError(f"Review with ID {review_id} not found")
        
            # Remove from place's reviews list if place exists
            place = self.place_repo.get(review.place_id)
            if place and review in place.reviews:
                place.reviews.remove(review)
        
            # Delete from repository
            self.review_repo.delete(review_id)
            return True
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error deleting review {review_id}: {e}")
            raise Exception("Failed to delete review")
