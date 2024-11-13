from flask import Blueprint
from flask_restx import Api

from app.api.v1.places import api as places_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint)

# Registering the places API
api.add_namespace(places_api)
