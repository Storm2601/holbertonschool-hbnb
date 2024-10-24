#!/usr/bin/python3

"""Amenity endpoints for the HBnB API."""

from flask_restx import Namespace # type: ignore

api = Namespace('amenities', description='Amenity operations')

# Placeholder for future operations (POST, GET, PUT)

from flask_restx import fields # type: ignore

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})
