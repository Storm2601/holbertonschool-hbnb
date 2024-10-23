#!/usr/bin/python3

# Importing UUID for unique identifiers
import uuid
# Importing datetime for timestamps
from datetime import datetime
# Importing User class from user module
from user import User
# Importing base_model class from Basemodel module
from .base_model import BaseModel
# Importing Place class from place module
from place import Place


class Review(BaseModel):
    """Class representing a review of a place"""

    def __init__(self, text, rating, place, user):
        """Initialize a Review instance with text, rating, 
        place, and user"""
        super().__init__()
        # Review text content
        self.text = text
        # Rating score
        self.rating = rating
        # Place being reviewed
        self.place = place
        # User who wrote the review
        self.user = user
        # Validate all fields on creation
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        # Ensure review text is provided
        if not self.text:
            raise ValueError("Review text is required")
        # Ensure rating is between 1 and 5
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        # Ensure text length does not exceed 500 characters
        if len(self.text) > 500:
            raise ValueError("Review text must not exceed 500 characters")
        # Ensure place is a valid Place instance
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a valid Place instance")
        # Ensure user is a valid User instance
        if not isinstance(self.user, User):
            raise ValueError("User must be a valid User instance")

    @staticmethod
    def is_unique_review(user, place, reviews):
        """Check if the user has already reviewed the place"""
        return all(
            review.user != user or review.place != place
            for review in reviews
        )
