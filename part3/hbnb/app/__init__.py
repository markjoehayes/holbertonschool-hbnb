from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
load_dotenv()
jwt = JWTManager()

def create_app(config_class=None):
    """Application factory function that returns configured flask app instance"""

    # Environment detection logic
    if config_class is None:
        # Get environement from environement variable, default = 'development'
        env = os.getenv('FLASK_ENV', 'development').lower()

        if env == 'production':
            config_class = 'config.ProductionConfig'
            print("Loading Production Configuration")
        elif env == 'testing':
            config_class = 'config.TestingConfig'
            print("Loading Testing Configuration")
        else: 
            config_class = 'config.DevelopmentConfig'
            print("Loading Development Configuration")


    app = Flask(__name__)
    # load configuration from the specified class
    try:
        app.config.from_object(config_class)
        print(f"Configuartion loaded: {config_class}")
    except ImportError as e:
        raise ValueError(f"Invalid configuration class: {config_class}. Error: {e}")
    # Initialize API
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API', 
              doc='/api/v1/')

    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register namespaces
    from app.api.v1.users import api as users_ns
    form app.api.v1.auth import as auth_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='api/v1/auth')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
        
    return app
