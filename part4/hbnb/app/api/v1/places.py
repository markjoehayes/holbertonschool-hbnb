# api/v1/places.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize Namespaces and facade
api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Model for swagger docs
place_model = api.model('Place', {
    'id': fields.String(readOnly=True),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Place price'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner ID'),
    'created_at': fields.String,
    'updated_at': fields.String
})

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

#---------------------------------
# ROUTES
#--------------------------------

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


@api.route('/')
class PlaceList(Resource):
    # Public - no authentication needed
    @api.response(200, 'List of all places')
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places (public)"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @jwt_required()
    @api.expect(place_model, validate=False)
    def post(self):
        """Create a new place (protected)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload or {}
        
        # Add owner_id from token
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 201
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    # Public - no authentication needed
    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get specific place (public)"""
        try:
            print(f"[DEBUG] Getting place ID: {place_id}")
            place = facade.get_place(place_id)
            print(f"[DEBUG] Found place: {place}")
            result = place.to_dict()
            print(f"[DEBUG] Serialized: {result}")
            return result, 200
        except ValueError as e:
            print(f"[DEBUG] ValueError: {e}")
            return {'error': str(e)}, 404
        except Exception as e:
            import traceback
            traceback.print_exc()
            api.abort(500, f"Internal server error: {str(e)}")


    @jwt_required()
    @api.expect(place_model, validate=False)
    def put(self, place_id):
        """Update a place (protected - owner only)"""
        current_user_id = get_jwt_identity()
        update_data = api.payload or {}
        
        # Check if place exists and user owns it
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            if str(place.owner_id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403

        # Update the place
        
            updated_place = facade.update_place(place_id, update_data)
            return updated_place.to_dict(), 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (protected — owner only)"""
        current_user_id = get_jwt_identity()

        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            if str(place.owner_id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403

            facade.place_repo.delete(place_id)
            return {'message': 'Place deleted successfully'}, 200

        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
