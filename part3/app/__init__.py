from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app.api.v1.users import api as users_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)

    # Initialize the API with version and description
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Configure the app using the provided config class
    app.config.from_object(config_class)

    # Initialize bcrypt
    bcrypt.init_app(app)

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
