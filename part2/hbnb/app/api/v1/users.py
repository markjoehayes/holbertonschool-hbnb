from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from werzeug.exceptions import BadRequest

api = Namespace('users', description='User operations')

#Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description = 'First name of user'),
    'last_name': fields.String(required=True, description='Email of user')
})

@api.route('/')
class UsersList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')

    def post(self):
    """R``egister a new user"""
    user_data = api.payload

    #check if email is already registered
    if existing_user:
        return {'error': 'Email already registered'}, 400
    try:
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
    except ValueError as e:
        return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get a list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')

class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.last_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input or email already registered')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        update_data = api.payload

        try:
            updated_user = facade.update_user(user_id, update_data)
            if not update_user:
                return {'error': 'User not found'}, 404

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': update_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


