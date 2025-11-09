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
    @api.expect(login_model)
    def post(self):
        credentials = api.payload
        print("=== DEBUG START ===")
        print(f"Looking up: {credentials['email']}")
        
        try:
            user = facade.get_user_by_email(credentials['email'])
            print(f"SUCCESS: User found - {user is not None}")
            if user:
                print(f"User ID: {user.id}")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            user = None
        
        if not user:
            print("FAIL: No user found")
            return {'error': 'Invalid credentials'}, 401
            
        print("DEBUG END ===")
        access_token = create_access_token(identity=str(user.id))
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
