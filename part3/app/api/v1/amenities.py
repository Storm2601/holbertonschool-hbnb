#!/usr/bin/python3

"""Amenity endpoints for the HBnB API."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.services.facade import HBnBFacade
from datetime import timedelta

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

# Facade to interact with data
facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @jwt_required()  # Protect this route with JWT authentication
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload

        # Check if amenity name is unique
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already exists'}, 400

        # Create the amenity
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
    @jwt_required()  # Protect this route with JWT authentication
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

    @jwt_required()  # Protect this route with JWT authentication
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

    @jwt_required()  # Protect this route with JWT authentication
    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.delete_amenity(amenity_id)  # Call to delete the amenity
        return {'message': 'Amenity successfully deleted'}, 200
