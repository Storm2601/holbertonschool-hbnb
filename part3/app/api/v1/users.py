#!/usr/bin/python3

"""User endpoints for the HBnB API."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

# Facade to interact with data
facade = HBnBFacade()

# Initialize Flask-JWT-Extended
# app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète'  # Utilisez une clé secrète sécurisée pour la production
# jwt = JWTManager(app)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Validate the email uniqueness using the User model method
        if not User.is_unique_email(user_data['email']):
            return {'error': 'Email is already taken, please choose another one'}, 400

        # Hash the password before creating the user
        password_hash = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_data['password'] = password_hash

        # Create the user with the hashed password
        new_user = facade.create_user(user_data)

        # Return user info without the password
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User logged in successfully')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Login a user and return a JWT token"""
        user_data = api.payload

        # Chercher l'utilisateur dans la base de données par email
        user = facade.get_user_by_email(user_data['email'])
        if not user:
            return {'error': 'Invalid credentials'}, 401

        # Vérifier le mot de passe
        if not bcrypt.check_password_hash(user.password, user_data['password']):
            return {'error': 'Invalid credentials'}, 401

        # Créer un jeton JWT pour l'utilisateur
        access_token = create_access_token(identity=user.id)
        
        return {'access_token': access_token}, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'You are not authorized to update this user')
    @jwt_required()  # Sécuriser cet endpoint avec JWT
    def put(self, user_id):
        """Update user details by ID"""
        current_user_id = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du jeton
        if current_user_id != user_id:
            return {'error': 'You are not authorized to update this user'}, 403

        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)

        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    @api.response(403, 'You are not authorized to delete this user')
    @jwt_required()  # Sécuriser cet endpoint avec JWT
    def delete(self, user_id):
        """Delete user by ID"""
        current_user_id = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du jeton
        if current_user_id != user_id:
            return {'error': 'You are not authorized to delete this user'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return {'message': 'User deleted successfully'}, 200
