from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

bcrypt = Bcrypt()
load_dotenv()

def create_app(config_class="config.DevelopmentConfig"):
    """Application factory function that returns configured flask app istance"""
    app = Flask(__name__)
    # load configuration from the specified class
    app.config.from_object(config_class)
    # Initialize API
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API', 
              doc='/api/v1/')

    bcrypt.init_app(app)

    # Import and register namespaces
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
        
    return app
