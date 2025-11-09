# api/v1/places.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize facade
facade = HBnBFacade()

api = Namespace('places', description='Place operations')

# Response model for place reviews
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route('/')
class PlaceList(Resource):
    # Public - no authentication needed
    def get(self):
        """Get all places (public)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @jwt_required()
    def post(self):
        """Create a new place (protected)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        
        # Set the owner to current user
        place_data['owner_id'] = current_user_id
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    # Public - no authentication needed
    def get(self, place_id):
        """Get specific place (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    def put(self, place_id):
        """Update a place (protected - owner only)"""
        current_user_id = get_jwt_identity()
        
        # Check if place exists and user owns it
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Update the place
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
