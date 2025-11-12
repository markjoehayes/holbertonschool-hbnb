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
    Facde layer for the Hbnb app.
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
#            raw_password = user_data.get("password")
#            if not raw_password:
#                raise ValueError("Password is required")

            # Hash the password
#            hashed_password_bytes = bcrypt.generate_password_hash(raw_password)
#            hashed_password = hashed_password_bytes.decode('utf-8')

            # Create the user and include the hashed password
            user = User(
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                email=user_data.get('email', ''),
                password=user_data.get('password', '')
            )

            print(f"[facade.create_user] Created User: {user.email}")

            storage.new(user)
            storage.save()
            return user

        except Exception as e:
            print(f"[facade.create_user] EXCEPTION: {e}")
            raise

#    def create_user(self, user_data):
#        """Create a new user with hashed password"""
        #user = User(**user_data) #change for security reasons
#        try:
#            hashed_password_bytes = bcrypt.generate_password_hash(user_data['password'])
 #           try:
 #               hashed_password = hashed_password_bytes.decode('utf-8')
 #           except AttributeError:
#                hashed_password = hashed_password_bytes

#            user = User(
#                first_name=user_data['first_name'],
#                last_name=user_data['last_name'],
#                email=user_data['email'],
#                password=hashed_password
#            )
            # DEBUG: show object before saving
 #           print(f"[facade.create_user] created User instance: id={getattr(user,'id',None)}, "
  #                f"email={getattr(user, 'email', None)}, first={getattr(user,'first_name', None)}")
            # Explicitly persist to in-memory storage
 #           storage.new(user)
 #           storage.save()
 #           print(f"[facade.create_user] storage.new() called; now srorage contains: ")
 #           for k, v in storage.all().items():
 #               print(f" {k} -> id={getattr(v, 'id', None)} email={getattr(v, 'email', None)}")


#        self.user_repo.add(user)
#        try:
#            storage.save()  # persist change globally!
#        except Exception as e:
#            print(f"[facade.create_user] storage.save() failed: {e}")
#            return user
#        except Exception as e:
#            print(f"[facade.create_user] EXCEPTION: {e}")
#            raise

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
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
    
        user.save()
        return user

    #-------------------
    # AMENITY METHODS
    #------------------

    def create_amenity(self, amenity_data):
        """Creates a new amenity with validation"""
        try:
            if not amenity_data or 'name' not in amenity_data:
                raise ValueError("Amenity name is required")

            name = amenity_data.get('name', '').strip()
            if not name:
                raise ValueError("Amenity name cannot be empty")
            
            # check if amenity with same name already exists
            existing = self.get_all_amenities()
            for amenity in existing:
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
        return self.amenity_repo.get_by_id(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Update an existing amenity"""
        return self.amenity_repo.update(amenity_id, data)


    #----------------------
    # PLACE METHODS
    #---------------------

    def create_place(self, place_data):
        """Create a new place with validation"""
        try:
            # Validate required fields
            #required_fields = ['title', 'price', 'owner_id']
            #for field in required_fields:
            #    if field not in place_data:
            #        raise ValueError(f"{field} is required")

            # Normalize field naming between API and model
            name = place_data.get("title") or place_data.get("name")
            if not name:
                raise ValueError("Place name (or title) is required")
            if "owner_id" not in place_data:
                raise ValueError("owner_id is required")
            if "price" not in place_data:
                raise ValueError("price is required")

            # Create new place - this will trigger validation in the Place class
            new_place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data.get('price'),
                latitude=place_data.get('latitude', 0.0),
                longitude=place_data.get('longitude', 0.0),
                owner_id=place_data['owner_id']
            )
            
            # Persist to storage
            new_place.save()

            print(f"[facade.create_place] Created place: {new_place.title} (id={new_place.id})")
            return new_place

            # Handle amenities if provided
            #if 'amenities' in place_data:
            #    for amenity_id in place_data['amenities']:
            #        pass

            # Save to repository
            #self.place_repo.add(new_place)
            #return new_place

        except Exception as e:
            raise e
        except Exception as e:
            print(f"[facade.create_place] Error: {e}")
            raise Exception("Failed to create place")

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all Places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        return self.place_repo.update(place_id, data)

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
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()
        
    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place"""
        # Get all reviews and filter by place_id
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]
        
    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.update(review_id, review_data)

#create a single global instance
facade = HBnBFacade()
