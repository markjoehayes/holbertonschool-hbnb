from app import bcrypt
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    unset_jwt_cookies
)
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# ---------------- LOGIN ----------------
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate a user and return a JWT token"""
        try:
            data = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                return {"error": "Email and password required"}, 400

            email = data['email']
            password = data['password']

            # Use facade method to get user from the real DB
            user = facade.get_user_by_email(email)

            if not user:
                return {"error": "Invalid credentials"}, 401

            # Check password
            if not bcrypt.check_password_hash(user.password, password):
                return {"error": "Invalid credentials"}, 401

            # Create JWT token
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        except Exception as e:
            print(f"[Login.post] EXCEPTION: {e}")
            return {"error": "Internal server error"}, 500

# ---------------- PROTECTED ----------------
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        # Add admin claim if you have it
        # For now, just return False
        is_admin = False
        return {
            'message': f'Hello, user {current_user}',
            'is_admin': is_admin
        }, 200

# ---------------- LOGOUT ----------------
@api.route('/logout')  # lowercase and consistent with /login
class Logout(Resource):
    def post(self):
        response = jsonify({"message": "Logged out successfully"})
        unset_jwt_cookies(response)
        return response, 200

