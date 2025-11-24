from flask import Blueprint
from flask_restx import Api

# Create blueprint WITHOUT url_prefix
api_bp = Blueprint('api', __name__)
api = Api(api_bp, title='HBNB API', version='1.0', description='HBNB REST API')
# Import the API models BEFORE resources
from app.api.v1.users import user_model, user_update_model
from app.api.v1.auth import login_model
from app.api.v1.places import place_model
from app.api.v1.amenities import amenity_model
from app.api.v1.reviews import review_model

# Register API models
api.models[user_model.name] = user_model
api.models[user_update_model.name] = user_update_model
api.models[login_model.name] = login_model
api.models[place_model.name] = place_model
api.models[amenity_model.name] = amenity_model
api.models[review_model.name] = review_model


# Import your resources
from app.api.v1.users import UserList, UserResource
from app.api.v1.auth import Login, ProtectedResource, Logout
from app.api.v1.places import PlaceList, PlaceResource
from app.api.v1.amenities import AmenityList, AmenityResource
from app.api.v1.reviews import ReviewList, ReviewResource

# Register resources
api.add_resource(UserList, '/users/', endpoint='users_list')
api.add_resource(UserResource, '/users/<user_id>', endpoint='users_resource')

api.add_resource(Login, '/auth/login', endpoint='auth_login')
api.add_resource(Logout, '/auth/logout', endpoint='auth_logout')
api.add_resource(ProtectedResource, '/auth/protected', endpoint='auth_protected')

api.add_resource(PlaceList, '/places/', endpoint='places_list')
api.add_resource(PlaceResource, '/places/<string:place_id>', endpoint='places_resource')

api.add_resource(AmenityList, '/amenities/', endpoint='amenities_list')
api.add_resource(AmenityResource, '/amenities/<amenity_id>', endpoint='amenities_resource')

api.add_resource(ReviewList, '/reviews/', endpoint='reviews_list')
api.add_resource(ReviewResource, '/reviews/<review_id>', endpoint='reviews_resource')

