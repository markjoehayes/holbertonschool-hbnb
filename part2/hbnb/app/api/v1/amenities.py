from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.services.facade import HBnBFacade

# Initialize facade
facade = HBnBFacade()

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Response model for returned amenities
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='last update tiemstamp')
    })

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model, code=201)
    def post(self):
        """Register a new amenity"""
        try:
            data = request.get_json()

            # validate input
            if not data or 'name' not in data:
                api.abort(400, 'Name is required')

            # create amenity using facade
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal Server Error: {str(e)}')

    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as e:
            api.abort(500, f'Internal Server Error: {str(e)}')

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, f'Amenity with ID {amenity_id} not found')
            return amenity.to_dict(), 200
        
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f'Internal Server Error: {str(e)}')
        

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
           data = request.get_json()

           # Validate input
           if not data:
               api.abort(400, 'No input data provided')

           if 'name' not in data:
               api.abort(400, 'Name is required for update')

           # Update amenity using facade
           amenity = facade.update_amenity(amenity_id, data)
           if not amenity:
               api.abort(404, f'Amenity with ID {amenity_id} not found')

           return amenity.to_dict(), 200

        except ValueError as e:
            # Handle both validation errors and not found errors
            if 'not found' in str(e).lower():
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
