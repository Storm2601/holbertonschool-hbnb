#!/usr/bin/python3

# Importing UUID for unique identifiers
import uuid
# Importing datetime for timestamps
from datetime import datetime
# Regular expression module for email validation
import re


# Base class for common attributes
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
        """Update the attributes of the object based
        on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                # Update the updated_at timestamp
                self.save()


class User(BaseModel):
    """Class representing a user in the system"""

    users = []  # Class variable to keep track of all users

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a User instance with name and email"""
        super().__init__()
        # User's first name
        self.first_name = first_name
        # User's last name
        self.last_name = last_name
        # User's email address
        self.email = email
        # Indicates if the user has admin privileges
        self.is_admin = is_admin
        # Validate all fields on creation
        self.validate_fields()
        # Add the user to the class list
        User.users.append(self)

    def validate_fields(self):
        """Validate that fields meet the required constraints"""
        # Ensure the email is not empty before applying other validations
        if not self.email:
            raise ValueError("Email is required")
        # Ensure first_name, last_name, and email are not empty
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        # Ensure first_name and last_name have at least 1 character
        if len(self.first_name) < 1 or len(self.last_name) < 1:
            raise ValueError("First name and last name must have at least 1 character")
        # Ensure first_name and last_name do not exceed 50 characters
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        # Validate the email format and uniqueness
        if not self.validate_email(self.email):
            raise ValueError("Email must be valid")
        if not self.is_unique_email(self.email):
            raise ValueError("Email must be unique")

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        # Regular expression for validating email
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    @classmethod
    def is_unique_email(cls, email):
        """Check if the provided email is unique among all users"""
        return all(user.email != email for user in cls.users)

    def delete_user(self):
        """Remove the user from the system"""
        try:
            User.users.remove(self)
            # Log the deletion of the user
            print(f"User {self.first_name} {self.last_name} has been deleted.")
        except ValueError:
            print("User not found.")
