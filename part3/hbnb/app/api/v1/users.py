from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from app.models.user import User
from app.models.storage import storage
from app.services import facade
from app.services.facade import HBnBFacade
from app import bcrypt

# Initialize facade
facade = HBnBFacade()

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
            print(f"🔧 DEBUG 1: Received user data: {user_data}")
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    print(f"❌ DEBUG: Missing field {field}")
                    return {'error': f'Missing required field: {field}'}, 400

            print("✅ DEBUG 2: All required fields present")
            
            # Check email uniqueness
            print(f"🔍 DEBUG 3: Checking email uniqueness for: {user_data['email']}")
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                print(f"❌ DEBUG: Email already exists")
                return {'error': 'Email already registered'}, 400
            
            print("✅ DEBUG 4: Email is unique")

            # Hash the password
            print("🔐 DEBUG 5: Hashing password...")
            try:
                password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                print(f"✅ DEBUG: Password hash created: {password_hash[:20]}...")
            except Exception as e:
                print(f"❌ DEBUG: Password hashing failed: {e}")
                raise

            # Create user data with hashed password
            user_data_with_hash = {
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': password_hash
            }
            print(f"📝 DEBUG 6: Prepared user data: {user_data_with_hash}")

            # Create a user using facade
            print("👤 DEBUG 7: Calling facade.create_user()...")
            try:
                new_user = facade.create_user(user_data_with_hash)
                print(f"✅ DEBUG: facade.create_user() returned: {new_user}")
                
                if new_user is None:
                    print("❌ DEBUG: facade.create_user() returned None!")
                    return {'error': 'Failed to create user'}, 500
                    
                print(f"🔍 DEBUG 8: New user attributes:")
                print(f"   - ID: {getattr(new_user, 'id', 'MISSING')}")
                print(f"   - First name: {getattr(new_user, 'first_name', 'MISSING')}")
                print(f"   - Last name: {getattr(new_user, 'last_name', 'MISSING')}")
                print(f"   - Email: {getattr(new_user, 'email', 'MISSING')}")
                print(f"   - Password: {getattr(new_user, 'password', 'MISSING')}")
                
            except Exception as e:
                print(f"❌ DEBUG: facade.create_user() raised exception: {e}")
                import traceback
                print(f"📜 DEBUG: Traceback from facade:\n{traceback.format_exc()}")
                raise

            # Try to call to_dict()
            print("📋 DEBUG 9: Calling to_dict()...")
            try:
                user_dict = new_user.to_dict()
                print(f"✅ DEBUG: to_dict() result: {user_dict}")
            except Exception as e:
                print(f"❌ DEBUG: to_dict() failed: {e}")
                # Create manual response as fallback
                user_dict = {
                    'id': getattr(new_user, 'id', None),
                    'first_name': getattr(new_user, 'first_name', None),
                    'last_name': getattr(new_user, 'last_name', None),
                    'email': getattr(new_user, 'email', None),
                    'created_at': getattr(new_user, 'created_at', None),
                    'updated_at': getattr(new_user, 'updated_at', None)
                }
                print(f"🔄 DEBUG: Using manual dict: {user_dict}")

            user_dict['message'] = 'User created successfully'
            print(f"🎉 DEBUG 10: Final response ready")
            
            return user_dict, 201

        except Exception as e:
            print(f"💥 DEBUG 11: TOP-LEVEL EXCEPTION: {str(e)}")
            import traceback
            print(f"📜 DEBUG 12: FULL TRACEBACK:\n{traceback.format_exc()}")
            return {'error': f'Internal server error: {str(e)}'}, 500

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
