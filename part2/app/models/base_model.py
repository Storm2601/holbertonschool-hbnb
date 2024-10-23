#!/usr/bin/python3

# Importing UUID for unique identifiers
import uuid
# Importing datetime for timestamps
from datetime import datetime


class BaseModel:
    """Base class providing common attributes and methods"""

    def __init__(self):
        """Initialize the BaseModel with ID and timestamps"""
        # Unique identifier for the instance
        self.id = str(uuid.uuid4())
        # Timestamp of creation
        self.created_at = datetime.now()
        # Timestamp of last update
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                # Update the updated_at timestamp
                self.save()
