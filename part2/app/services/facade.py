#!/usr/bin/python3

"""Facade for managing user operations."""

from app.models.user import User
from part2.app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Facade class to manage user operations."""

    def __init__(self):
        """Initialize the facade with the user repository."""
        self.user_repo = InMemoryRepository()

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
