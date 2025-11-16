from app.models.storage import storage
from app import bcrypt
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from werkzeug.security import generate_password_hash
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade:
    """
    Facade layer for the Hbnb app.
    Refactotred to use SQLAlchemyRepository
    """

    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place) 
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
    
    #------------------
    # USER METHODS
    #-----------------

    def create_user(self, user_data):
        """Create a new user with hashed password"""
        try:
            user = User(
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                email=user_data.get('email', ''),
                password=user_data.get('password', '')
            )

            self.user_repo.add(user)
            return user

        except Exception as e:
            print(f"[facade.create_user] EXCEPTION: {e}")
            raise

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
    
        # Update allowed fields only
    
        for field in ("first_name", "last_name"):
            if field in user_data:
                setattr(user, field, user_data[field])

        user.save()
        return user

    #-------------------
    # AMENITY METHODS
    #------------------

    def create_amenity(self, amenity_data):
        """Creates a new amenity with validation"""
        try:
            name = amenity_data.get("name")
            if not name:
                raise ValueError("Amenity name is required")

            amenity = Amenity(
                name=name,
                description=amenity_data.get("description")
            )

            self.amenity_repo.add(amenity)
            return amenity

        except Exception as e:
            print(f"[facade.create_amenity] Error: {e}")
            raise

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get_by_id(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Update an existing amenity"""
        try:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")

            for key, value in amenity_data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)

            self.amenity_repo.update(amenity_id, amenity_data)
            print(f"[facade.update_amenity] Updated amenity {amenity_id}")
            return amenity

        except Exception as e:
            print(f"[facade.update_amenity] Error: {e}")
            raise

    #----------------------
    # PLACE METHODS
    #---------------------

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
                title=place_data.get("title"),
                description=place_data.get('description'),
                price=place_data.get('price'),
                latitude=place_data.get('latitude', 0.0),
                longitude=place_data.get('longitude', 0.0),
                owner_id=place_data['owner_id']
                )
            
            # Persist to storage
            self.place_repo.add(new_place)   
            return new_place

        except Exception as e:
            print(f"[facade.create_place] Error: {e}")
            raise 

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all Places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        try:
            place = self.place_repo.get(place_id)
            if not place:
                raise ValueError(f"Place with ID {place_id} not found")

            for key, value in place_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)

            # SQLAlchemy commit happens in repo.update()
            self.place_repo.update(place_id, place_data)

            print(f"[facade.update_place] Updated place {place_id}")
            return place

        except Exception as e:
            print(f"[facade.update_place] Error updating place: {e}")
            raise     
    #-------------------------
    # REVIEW METHODS
    #---------------------------


    def create_review(self, review_data):
        """Create a new review with validation"""
        try:
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in review_data:
                    raise ValueError(f"{field} is required")
        
            # Build Review object
            new_review = Review (
                    text=review_data['text'],
                    rating=review_data['rating'],
                    user_id=review_data['user_id'],
                    place_id=review_data['place_id']
            )

            self.review_repo.add(new_review)

            # Add review to place's reviews list
            #place.add_review(new_review)

            return new_review

        except Exception as e:
            print(f"Error creating review: {e}")
            raise 

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()
        
    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        return self.review_repo.filter_by(place_id=place_id)

    def update_review(self, review_id, review_data):
        """Update a review"""
        try:
            review = self.review_repo.get(review_id)
            if not review:
                raise ValueError(f"Review with ID {review_id} not found")

            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)

            self.review_repo.update(review_id, review_data)
            print(f"[facade.update_review] Updated review {review_id}")
            return review

        except Exception as e:
            print(f"[facade.update_review] Error: {e}")
            raise

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

#create a single global instance
facade = HBnBFacade()
