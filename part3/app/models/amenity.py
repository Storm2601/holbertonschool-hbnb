#!/usr/bin/python3

# Importing the Base and BaseModel classes
from .base_model import BaseModel
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Amenity(Base, BaseModel):
    """Class representing an amenity in the system"""
    __tablename__ = 'amenities'

    id = Column(String(60), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    def __init__(self, name, description=None):
        """Initialize an Amenity instance with name and an optional description"""
        super().__init__()
        self.name = name
        self.description = description
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        # Ensure name is not empty
        if not self.name:
            raise ValueError("Name is required")
        # Ensure name does not exceed 50 characters
        if len(self.name) > 50:
            raise ValueError("Name must not exceed 50 characters")
