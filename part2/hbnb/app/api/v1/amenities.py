from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services.exceptions import NotFoundError, ValidationError

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()
# Define the amenity model for Swagger documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='The amenity unique identifier'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            data = request.get_json()
            new_amenity = facade.create_amenity(data)
            return new_amenity, 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return amenities, 200
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return amenity, 200
        except NotFoundError:
            api.abort(404, 'Amenity not found')
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            data = request.get_json()
            if not data:
                api.abort(400, 'No input data provided')
                
            updated_amenity = facade.update_amenity(amenity_id, data)
            return {'message': 'Amenity updated successfully'}, 200
        except NotFoundError:
            api.abort(404, 'Amenity not found')
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))
