from app import bcrypt
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
    })

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = facade.get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity() # Retrieve the user's identitiy form the token
        additional_claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        return {
                'message': f'Hello, user {current_user}',
                'is_admin': is_admin
                }, 200
