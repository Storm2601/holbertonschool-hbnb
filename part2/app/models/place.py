#!/usr/bin/python3

# Importing the BaseModel class
from .base_model import BaseModel


class Place(BaseModel):
    """Class representing a place in the system"""

    def __init__(self, name, description, city, price_per_night):
        """Initialize a Place instance with name, description, and city"""
        super().__init__()
        # Place name
        self.name = name
        # Place description
        self.description = description
        # City where the place is located
        self.city = city
        # Price per night for the place
        self.price_per_night = price_per_night
        # Validate all fields on creation
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        # Ensure name and city are not empty
        if not self.name or not self.city:
            raise ValueError("Name and city are required")
        # Ensure description is not empty
        if not self.description:
            raise ValueError("Description is required")
        # Ensure price_per_night is a non-negative integer
        if not isinstance(self.price_per_night, int) or self.price_per_night < 0:
            raise ValueError("Price per night must be a non-negative integer")
