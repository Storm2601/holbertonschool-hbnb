#!/usr/bin/python3

"""Review endpoints for the HBnB API."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'place_id': fields.Integer(required=True, description='ID of the place being reviewed'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating for the place', min=1, max=5),
})

# Facade to interact with data
facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'User cannot review their own place')
    @jwt_required()  # Secure this endpoint with JWT
    def post(self):
        """Create a new review"""
        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        review_data = api.payload

        # Check if the user is trying to review their own place
        place_owner = facade.get_place_owner(review_data['place_id'])
        if place_owner and place_owner.id == user_id:
            return {'error': 'You cannot review your own place'}, 400

        # Check if the user has already reviewed the place
        existing_review = facade.get_review_by_user_and_place(user_id, review_data['place_id'])
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 400

        # Create the review
        review_data['user_id'] = user_id  # Associate the review with the logged-in user
        new_review = facade.create_review(review_data)

        return {
            'id': new_review.id,
            'place_id': new_review.place_id,
            'user_id': new_review.user_id,
            'text': new_review.text,
            'rating': new_review.rating
        }, 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'place_id': review.place_id,
            'user_id': review.user_id,
            'text': review.text,
            'rating': review.rating
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(403, 'You are not authorized to update this review')
    @jwt_required()  # Secure this endpoint with JWT
    def put(self, review_id):
        """Update review by ID"""
        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        review_data = api.payload

        # Check if the review belongs to the current user
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != user_id:
            return {'error': 'You are not authorized to update this review'}, 403

        # Update the review
        updated_review = facade.update_review(review_id, review_data)
        return {
            'id': updated_review.id,
            'place_id': updated_review.place_id,
            'user_id': updated_review.user_id,
            'text': updated_review.text,
            'rating': updated_review.rating
        }, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'You are not authorized to delete this review')
    @jwt_required()  # Secure this endpoint with JWT
    def delete(self, review_id):
        """Delete review by ID"""
        user_id = get_jwt_identity()  # Get the user ID from the JWT token

        # Check if the review belongs to the current user
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != user_id:
            return {'error': 'You are not authorized to delete this review'}, 403

        # Delete the review
        facade.delete_review(review_id)
        return {'message': 'Review successfully deleted'}, 200
