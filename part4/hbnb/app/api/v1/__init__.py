from flask_restx import Api
from flask import Blueprint

# create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# initialize Flask-RESTX API
api = Api(api_bp, title='HBNB API', version='1.0', description='HBNB REST API')

# import your resource definitions
from app.api.v1.users import UserList  # adjust path if needed

# register your resources
api.add_resource(UserList, '/users/', endpoint='users')

