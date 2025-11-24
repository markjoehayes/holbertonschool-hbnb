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
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = facade.get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

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

