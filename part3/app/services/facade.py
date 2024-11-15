#!/usr/bin/python3

"""Facade for managing user operations."""

from app.models.user import User
from app.models.place import Place  # Importer la classe Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Facade class to manage user operations."""

    def __init__(self):
        """Initialize the facade with the user repository."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user and add it to the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID from the repository."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email from the repository."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update a user's details by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            return None  # Return None if the user is not found
        for key, value in user_data.items():
            setattr(user, key, value)  # Update the user attributes dynamically
        return user

    def create_place(self, place_data): 
        """Create a new place and add it to the repository."""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID from the repository."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places from the repository."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None  # Place not found
        for key, value in place_data.items():
            setattr(place, key, value)  # Update place attributes
        return place

    def delete_place(self, place_id):
        """Delete a place from the system"""
        place = self.get_place(place_id)
        if place:
            self.place_repo.remove(place)
            return True
        return False

    def get_amenity_by_name(self, name):
        """Fetch an amenity by its name."""
        return next((amenity for amenity in Amenity.amenities if amenity.name == name), None)

    def create_amenity(self, amenity_data):
        """Create a new amenity in the system."""
        new_amenity = Amenity(name=amenity_data['name'], description=amenity_data.get('description'))
        return new_amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return Amenity.amenities

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID."""
        return Amenity.find_by_id(amenity_id)

    def update_amenity(self, amenity_id, amenity_data):
        """Update the amenity's information."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.name = amenity_data.get('name', amenity.name)
        amenity.description = amenity_data.get('description', amenity.description)
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete an amenity from the system."""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            Amenity.amenities.remove(amenity)
            return True
        return False
