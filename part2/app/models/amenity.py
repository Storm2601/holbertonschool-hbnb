#!/usr/bin/python3

# Importing the BaseModel class
from .base_model import BaseModel


class Amenity(BaseModel):
    """Class representing an amenity in the system"""

    def __init__(self, name, description=None):
        """Initialize an Amenity instance with name and an optional description"""
        super().__init__()
        # Amenity name
        self.name = name
        # Optional description of the amenity
        self.description = description
        # Validate all fields on creation
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        # Ensure name is not empty
        if not self.name:
            raise ValueError("Name is required")
        # Ensure name does not exceed 50 characters
        if len(self.name) > 50:
            raise ValueError("Name must not exceed 50 characters")
