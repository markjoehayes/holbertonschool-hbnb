from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from app.models.user import User
from app.models.storage import storage
from app.services import facade
from app import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize facade
#facade = HBnBFacade()

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
    })

# Response model (without password)
user_response_model = api.model('UserResponse', {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='First name of user'),
        'last_name': fields.String(description='Last name of user'),
        'email': fields.String(description='Email of the user'),
        'created_at': fields.String(description='Creation timestamp'),
        'updated_at': fields.String(description='Last update timestamp'),
        'message': fields.String(description='Success message')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
    })

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid Input data')
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            print(f"DEBUG 1: Received user data: {user_data}")
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    print(f"DEBUG: Missing field {field}")
                    return {'error': f'Missing required field: {field}'}, 400

            print("DEBUG 2: All required fields present")
            
            # Check email uniqueness
            print(f"DEBUG 3: Checking email uniqueness for: {user_data['email']}")
#            existing_user = facade.get_user_by_email(user_data['email'])
#            if existing_user:
#                print(f"DEBUG: Email already exists")
#                return {'error': 'Email already registered'}, 400
#            
#            print("DEBUG 4: Email is unique")
#
            # Hash the password
#            print("DEBUG 5: Hashing password...")
#            try:
#                password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
#                print(f"DEBUG: Password hash created: {password_hash[:20]}...")
#            except Exception as e:
#                print(f" DEBUG: Password hashing failed: {e}")
#                raise

            # Create user data with hashed password
 #           user_data_with_hash = {
 #               'first_name': user_data['first_name'],
 #               'last_name': user_data['last_name'],
 #               'email': user_data['email'],
 #               'password': password_hash
 #           }

            # Create a user using facade
#            try:
#                new_user = facade.create_user(user_data_with_hash)
                
#                if new_user is None:
#                    return {'error': 'Failed to create user'}, 500
                    
                
#            except Exception as e:
#                print(f"DEBUG: facade.create_user() raised exception: {e}")
#                import traceback
#                raise

            # Try to call to_dict()
#            try:
#                user_dict = new_user.to_dict()
#            except Exception as e:
                # Create manual response as fallback
#                user_dict = {
#                    'id': getattr(new_user, 'id', None),
#                    'first_name': getattr(new_user, 'first_name', None),
#                    'last_name': getattr(new_user, 'last_name', None),
#                    'email': getattr(new_user, 'email', None),
#                    'created_at': getattr(new_user, 'created_at', None),
#                    'updated_at': getattr(new_user, 'updated_at', None)
#                }
#                print(f"DEBUG: Using manual dict: {user_dict}")


            #  Check if email already exists (using SimpleStorage)
            existing_user = storage.get_by_email(User, user_data["email"]) if hasattr(storage, "get_by_email") else None
            if existing_user:
                print(f"DEBUG: Email already exists in SimpleStorage")
                return {'error': 'Email already registered'}, 400

            #  Create a new user object and store it
            print("DEBUG 7: Creating User instance and saving via SimpleStorage")
            new_user = User(**user_data_with_hash)
            storage.new(new_user)
            storage.save()  # currently a no-op, but keeps interface consistent
            print(f"DEBUG: Saved new user {new_user.email} with id {new_user.id}")

            user_dict['message'] = 'User created successfully'
            print(f"DEBUG 10: Final response ready")
            
            return user_dict, 201

        except Exception as e:
            print(f"DEBUG 11: TOP-LEVEL EXCEPTION: {str(e)}")
            import traceback
            print(f"DEBUG 12: FULL TRACEBACK:\n{traceback.format_exc()}")
            return {'error': f'Internal server error: {str(e)}'}, 500

    @api.response(200, 'List of all users')
    def get(self):
        """Retrieve all registered users"""
            
        try:
            users = facade.user_repo.get_all()
            user_list = [user.to_dict() for user in users]
            return user_list, 200
        except Exception as e:
            print(f"DEBUG: Error retrieving users: {e}")
            return {'error': 'Internal server error'}, 500

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'User not found')
    @api.marshal_with(user_response_model)
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, f'User with ID {user_id} not found')

            # Return user data without password (using to_dict() whicg excludes password )
            return user.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.expect(user_update_model)  # We'll create this model below
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.marshal_with(user_response_model)
    @jwt_required()  # ADD JWT PROTECTION
    def put(self, user_id):
        """Update user information (users can only update their own data)"""
        try:
            current_user_id = get_jwt_identity()  # Get current user from JWT
            
            # Check if user is modifying their own data
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            data = request.get_json()
            if not data:
                return {'error': 'No input data provided'}, 400

            # Prevent email and password modification
            if 'email' in data:
                return {'error': 'You cannot modify email'}, 400
            if 'password' in data:
                return {'error': 'You cannot modify password'}, 400

            # Update user using facade
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            return updated_user.to_dict(), 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500
