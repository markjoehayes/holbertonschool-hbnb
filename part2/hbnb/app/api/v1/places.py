from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services.exceptions import NotFoundError, ValidationError

api = Namespace('places', description='Place operations')

# Models for relationships
user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

# Main place model
place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})

place_response_model = api.inherit('PlaceResponse', place_model, {
    'id': fields.String,
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model))
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """Create a new place"""
        try:
            facade = HBnBFacade()
            return facade.create_place(api.payload), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.marshal_list_with(place_response_model)
    def get(self):
        """List all places"""
        try:
            return HBnBFacade().get_all_places()
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """Get place details"""
        try:
            return HBnBFacade().get_place(place_id)
        except NotFoundError:
            api.abort(404, "Place not found")
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(place_model)
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """Update a place"""
        try:
            return HBnBFacade().update_place(place_id, api.payload)
        except NotFoundError:
            api.abort(404, "Place not found")
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))
