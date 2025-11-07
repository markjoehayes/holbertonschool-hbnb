from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from app.models.user import User
from app.models.storage import Storage
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
        'updated_at': fields.String(description='Last update timestamp')
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
            # validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    return {'error': f'Missing required field: {field}'}, 400

            #Simulate email unniqueness check(to be replaced by real validation with persistence)
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Hash the password before creating user
            password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

            # Create user data with hashed password
            user_data_with_hash = {
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': usrer_data['email'],
                    'password': password_hash # pass hash inplace of plaintext pw
            }

            # create a user using facade
            new_user = facade.create_user(user_data_with_hash)
            return new_user.to_dict(), 201

        except Exception as e:
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
