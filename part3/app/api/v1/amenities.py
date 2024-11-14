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

from flask_restx import Resource # type: ignore
from app.services.facade import HBnBFacade

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload

        # Simulate uniqueness check for amenity name (to be replaced with persistence validation)
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already exists'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': new_amenity.description
        }, 201

    @api.response(200, 'Amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [ 
            {'id': a.id, 'name': a.name, 'description': a.description} 
            for a in amenities 
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity details by ID"""
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            'description': updated_amenity.description
        }, 200