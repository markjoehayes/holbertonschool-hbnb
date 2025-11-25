# api/v1/reviews.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Initialize facade
facade = HBnBFacade()

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
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
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Register a new review"""
        try:
            data = request.get_json()
            
            # Validate input
            if not data:
                api.abort(400, 'No input data provided')
            
            # Create review using facade
            review = facade.create_review(data)
            return review.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
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
            if not review:
                api.abort(404, f'Review with ID {review_id} not found')
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
    def put(self, review_id):
        """Update a review's information"""
        try:
            data = request.get_json()
            
            # Validate input
            if not data:
                api.abort(400, 'No input data provided')
            
            # Update review using facade
            review = facade.update_review(review_id, data)
            if not review:
                api.abort(404, f'Review with ID {review_id} not found')
            
            return review.to_dict(), 200
            
        except ValueError as e:
            # Handle both validation errors and not found errors
            if 'not found' in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            success = facade.delete_review(review_id)
            if not success:
                api.abort(404, f'Review with ID {review_id} not found')
            
            return {'message': 'Review deleted successfully'}, 200
            
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
