#!/usr/bin/python3

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Place(Base):
    """Class representing a place in the system"""
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    city = Column(String(128), nullable=False)
    price_per_night = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amenities = Column(String(1024), nullable=True)

    def __init__(self, name, description, city, price_per_night, latitude, longitude, owner_id, amenities):
        """Initialize a Place instance with name, description, city, and additional attributes"""
        self.name = name
        self.description = description
        self.city = city
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        if not self.name or not self.city:
            raise ValueError("Name and city are required")
        if not self.description:
            raise ValueError("Description is required")
        if not isinstance(self.price_per_night, (int, float)) or self.price_per_night < 0:
            raise ValueError("Price per night must be a non-negative float")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def to_dict(self):
        """Convert Place instance to dictionary format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'city': self.city,
            'price_per_night': self.price_per_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': self.amenities
        }
