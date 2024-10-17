#!/usr/bin/python3


# Importing the UUID module for generating unique identifiers
import uuid
# Importing the datetime module for handling timestamps
from datetime import datetime

# Importing BaseModel from the user module to inherit common
# attributes and methods
from part2.app.models.user import BaseModel


class Amenity(BaseModel):
    """Class representing an amenity for a place"""

    # Class variable to keep track of existing amenity names
    existing_amenity_names = set()

    def __init__(self, name):
        """Initialize an Amenity instance with a name.

        Args:
            name (str): The name of the amenity.

        Raises:
            ValueError: If the name is empty, exceeds 50 characters, is not a 
            string, or contains special characters.
        """
        super().__init__()
        # Name of the amenity
        self.name = name
        # Validate all fields upon creation
        self.validate_fields()
        # Add name to existing amenities
        self.add_to_existing_names()

    def validate_fields(self):
        """Validate that fields meet the required constraints.

        Raises:
            ValueError: If the amenity name is empty, exceeds 50 characters,
            is not a string, or contains special characters.
        """
        if not self.name:
            # Check for empty name
            raise ValueError("Amenity name is required")
        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        if not isinstance(self.name, str):
            # Ensure the name is a string
            raise ValueError("Amenity name must be a string")
        if any(char in self.name for char in ['!', '@', '#', '$', '%']):
            # Check for undesirable characters
            raise ValueError(
                "Amenity name must not contain special characters"
            )

    def add_to_existing_names(self):
        """Add the amenity name to the set of existing names if unique.

        Raises:
            ValueError: If the amenity name is not unique.
        """
        if self.name in Amenity.existing_amenity_names:
            raise ValueError("Amenity name must be unique")
        Amenity.existing_amenity_names.add(self.name)

    def __str__(self):
        """String representation of the amenity.

        Returns:
            str: String representing the instance of the Amenity class.
        """
        return f"Amenity({self.id}): {self.name}"
