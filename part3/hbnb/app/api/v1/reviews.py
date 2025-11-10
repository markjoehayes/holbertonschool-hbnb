# api/v1/reviews.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize facade
facade = HBnBFacade()

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Response model for returned reviews
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Cannot review your own place')
    @api.marshal_with(review_response_model, code=201)
    @jwt_required()
    def post(self):
        """Register a new review"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            # Validate input
            if not data:
                api.abort(400, 'No input data provided')

            # Validate required fields
            if 'text' not in data or 'rating' not in data or 'place_id' not in data:
                api.abort(400, 'Missing required fields: text, rating, or place_id')


            # ADD VALIDATION: Check if user owns the place
            place = facade.get_place(data['place_id'])
            if not place:
                api.abort(404, 'Place not found')

            if place.owner_id == current_user_id:
                api.abort(403, 'You cannot review your own place')

            # ADD VALIDATION: Check if user already reviewed this place
            existing_reviews = facade.get_reviews_by_place(data['place_id'])
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    api.abort(400, 'You have already reviewed this place')
            
            # prepare review data
            review_data = {
                    'text': data['text'],
                    'rating': data['rating'],
                    'user_id': current_user_id,
                    'place_id': data['place_id']
            }

            # create review using facade
            review = facade.create_review(review_data)
            return review.to_dict(), 201

            # Set the user_id from JWT token, not from request
            # data['user_id'] = current_user_id  # OVERRIDE with current user    
            
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            import traceback
            print("DEBUG TRACEBACK:\n", traceback.format_exc())
            api.abort(500, f'Internal server error: {str(e)}')

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_response_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            # Validate input
            if not data:
                api.abort(400, 'No input data provided')

             # ADD VALIDATION: Check if user owns the review
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, f'Review with ID {review_id} not found')
                
            updated = facade.update_review(review_id, data)
            return updated.to_dict(), 200

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        try:
            current_user_id = get_jwt_identity()

            # ADD VALIDATION: Check if user owns the review
            review = facade.get_review(review_id)
            if review.user_id != get_jwt_identity():
                api.abort(403, 'You can only delete your own reviews')

            success = facade.delete_review(review_id)
            if not success:
                api.abort(404, f'Review with ID {review_id} not found')

            return {'message': 'Review deleted successfully'}, 200

        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
