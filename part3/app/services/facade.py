#!/usr/bin/python3

"""Facade for managing user operations."""

from app.models.user import User
from app.models.place import Place  # Importer la classe Place
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
        user = self.user_repo.get(user_id)
        if not user:
            return None  # User not found
        for key, value in user_data.items():
            setattr(user, key, value)  # Update user attributes
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
