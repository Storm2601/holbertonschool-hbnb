#!/usr/bin/python3

# Importing UUID for unique identifiers
import uuid
# Importing datetime for timestamps
from datetime import datetime
# Importing SQLAlchemy components
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Review(Base):
    """Class representing a review of a place"""
    __tablename__ = 'reviews'

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place, user):
        """Initialize a Review instance with text, rating, 
        place, and user"""
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
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
            for review in reviews)
