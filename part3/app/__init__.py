from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import config

# ajout des extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name="default"):
    """Crée et configure l'application Flask."""
    
    # add l'appication Flask
    app = Flask(__name__)

    # uplowd la config depuis le fichier de config
    app.config.from_object(config[config_name])

    # initialiser extensions
    db.init_app(app)
    jwt.init_app(app)

    # créer l'objet api avec des config basiques
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # enregistrer les namespaces (utilisateur, places, etc.)
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
