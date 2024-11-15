from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager  # Importation du gestionnaire JWT
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns  # Si tu as un namespace pour les places
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)

    # Configure la clé secrète pour JWT
    app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète'  # Change cette clé pour quelque chose de sécurisé en production

    # Initialisation de l'API avec version et description
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Charger la configuration de l'application
    app.config.from_object(config_class)

    # Initialiser bcrypt
    bcrypt.init_app(app)

    # Initialiser JWT
    jwt = JWTManager(app)  # Initialisation du gestionnaire JWT

    # Enregistrer les namespaces API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')  # Assure-toi que tu as ce namespace pour les places
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
