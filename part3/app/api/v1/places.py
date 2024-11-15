#!/usr/bin/python3

"""Place endpoints for the HBnB API."""

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'owner_id': fields.String(required=True, description='ID of the place owner')
})

# Facade to interact with data
facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload

        # Check if the place owner exists (optional check depending on your system)
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 400

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'name': new_place.name,
            'description': new_place.description,
            'owner_id': new_place.owner_id
        }, 201

    @api.response(200, 'Places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [
            {'id': p.id, 'name': p.name, 'description': p.description, 'owner_id': p.owner_id}
            for p in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'name': place.name,
            'description': place.description,
            'owner_id': place.owner_id
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place details by ID"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)

        if not updated_place:
            return {'error': 'Place not found'}, 404

        return {
            'id': updated_place.id,
            'name': updated_place.name,
            'description': updated_place.description,
            'owner_id': updated_place.owner_id
        }, 200

    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'You are not authorized to delete this place')
    @jwt_required()  # Secure this endpoint with JWT
    def delete(self, place_id):
        """Delete place by ID"""
        user_id = get_jwt_identity()  # Get the user ID from the JWT token

        # Check if the place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check if the current user is the owner of the place
        if place.owner_id != user_id:
            return {'error': 'You are not authorized to delete this place'}, 403

        # Proceed to delete the place
        facade.delete_place(place_id)
        return {'message': 'Place successfully deleted'}, 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        # Obtention des informations de l'utilisateur courant depuis le JWT
        current_user = get_jwt_identity()

        # Définir is_admin à False par défaut si non existant
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        # Récupérer le lieu en question depuis la base de données
        place = facade.get_place(place_id)

        # Si le lieu n'existe pas, retourner une erreur
        if not place:
            return {'error': 'Place not found'}, 404

        # Vérification si l'utilisateur est admin ou s'il est le propriétaire du lieu
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # On récupère les données envoyées pour la mise à jour
        place_data = request.get_json()

        # Exemple de validation des données à mettre à jour
        if 'name' in place_data:
            place.name = place_data['name']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'location' in place_data:
            place.location = place_data['location']
        # Ajoutez d'autres champs selon les besoins

        # Appeler la fonction pour mettre à jour le lieu dans la base de données
        updated_place = facade.update_place(place)

        # Retourner la réponse avec les données mises à jour
        return {'message': 'Place updated successfully', 'place': updated_place.to_dict()}, 200
