#!/usr/bin/python3


# Importing BaseModel and User class from user module
from part2.app.models.user import BaseModel, User
# Importing Review class from review module
from part2.app.models.review import Review
# Importing Amenity class from amenity module
from part2.app.models.amenity import Amenity


class Place(BaseModel):
    """Class representing a place for rent"""

    def __init__(self, title, price, latitude, longitude,
                 owner, description=""):
        """Initialize a Place instance with title, price,
        coordinates, and owner"""
        super().__init__()
        # Place title
        self.title = title
        # Optional description
        self.description = description
        # Price per night
        self.price = price
        # Latitude coordinate
        self.latitude = latitude
        # Longitude coordinate
        self.longitude = longitude
        # Owner of the place (User instance)
        self.owner = owner
        # List to store related reviews
        self.reviews = []
        # List to store related amenities
        self.amenities = []
        # Validate all fields on creation
        self.validate_fields()

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        if self.price <= 0:
            raise ValueError("Price must be a positive value")
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        if not isinstance(self.owner, User):
            raise ValueError("Owner must be a valid User instance")
        if self.owner is None:
            raise ValueError("Owner is required and cannot be None")

        # Optional description length validation (if required)
        if len(self.description) > 255:
            raise ValueError("Description must not exceed 255 characters")

    def add_review(self, review):
        """Add a review to the place if it is a valid Review instance"""
        if not isinstance(review, Review):
            raise ValueError("Review must be a valid Review instance")
        if review in self.reviews:
            raise ValueError("Review already added to this place")
        # Append review to the list
        self.reviews.append(review)

    def list_reviews(self):
        """Return a list of all reviews associated with the place"""
        return self.reviews

    def add_amenity(self, amenity):
        """Add an amenity to the place if it is a valid Amenity instance"""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be a valid Amenity instance")
        if amenity in self.amenities:
            raise ValueError("Amenity already added to this place")
        # Check for uniqueness of amenity name
        if any(a.name == amenity.name for a in self.amenities):
            raise ValueError("Amenity name must be unique within this place")
        # Append amenity to the list
        self.amenities.append(amenity)

    def list_amenities(self):
        """Return a list of all amenities associated with the place"""
        return self.amenities
